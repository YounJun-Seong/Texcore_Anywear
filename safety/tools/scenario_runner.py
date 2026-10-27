"""정답표(scenarios/*) → 엔진 실행 → 일치 여부. 테스트와 일치율 보고서가 같이 쓴다."""
import csv
from pathlib import Path

import yaml

from safety_engine.codes import ActionKind
from safety_engine.emergency import EmergencyFlow
from safety_engine.precheck import allowance, post_check, pre_check
from safety_engine.session import SessionMonitor, hr_limits
from safety_engine.types import DoctorLimits, Profile, Vitals

SCENARIO_DIR = Path(__file__).resolve().parent.parent / "scenarios"


def _num(v):
    if v in ("", None):
        return None
    f = float(v)
    return int(f) if f.is_integer() else f


def _set(v):
    return frozenset(x for x in (v or "").split("|") if x)


def read_csv(path):
    with open(path, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def read_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


# ---- 운동 전 판정 ----
def run_precheck_row(rules, row):
    profile = Profile(
        age=int(row["age"]),
        conditions=_set(row["gate_conditions"]),
        parq_risk=row["parq_risk"] == "1",
        doctor_clearance=row["clearance"] == "1",
        device=row["device"] or None,
        doctor_limits=DoctorLimits(_num(row["dr_sbp_max"]), _num(row["dr_dbp_max"]),
                                   _num(row["dr_hr_max"]), _num(row["dr_hr_ceiling"])),
    )
    vitals = Vitals(_num(row["sbp"]), _num(row["dbp"]), _num(row["hr"]), row["bp_source"], row["hr_source"])
    d = pre_check(rules, profile, vitals, _set(row["symptoms"]), _set(row["conditions"]))
    missing = [c for c in _set(row["expected_codes"]) if c not in d.reasons]
    ok = d.outcome == row["expected"] and not missing
    got = d.outcome + (f" (사유 코드 누락: {missing})" if missing else "")
    return ok, got


# ---- 심박 상한 ----
def run_limits_row(rules, row):
    profile = Profile(age=int(row["age"]), beta_blocker=row["beta_blocker"] == "1", device=row["device"] or None,
                      doctor_limits=DoctorLimits(exercise_hr_ceiling=_num(row["dr_hr_ceiling"])))
    lim = hr_limits(rules, profile, int(row["weeks"]), row["escalation"] == "1", row["light"])
    ok = lim["ceiling"] == int(row["expected_ceiling"]) and lim["mode"] == row["expected_mode"]
    return ok, f"{lim['ceiling']} {lim['mode']}"


# ---- 운동 후·허용 범위 ----
def run_misc_row(rules, row):
    if row["kind"] == "post_check":
        got = post_check(rules, int(row["a"]), int(row["b"])).outcome
        return got == row["expected"], got
    got = allowance(rules, row["a"], int(row["b"]))["max_minutes"]
    return got == int(row["expected"]), str(got)


# ---- 운동 중 ----
def expand_events(events):
    out = []
    for i, e in enumerate(events):
        if "from" in e:
            kind = "hr" if "hr" in e else "tick"
            for t in range(e["from"], e["to"] + 1):
                out.append((t, i, kind, e.get("hr")))
        else:
            kind = next(k for k in ("rpe", "symptom", "user_stop", "interaction", "resume") if k in e)
            out.append((e["t"], i, kind, e[kind]))
    out.sort(key=lambda x: (x[0], x[1]))
    return [(t, kind, v) for t, _, kind, v in out]


def run_session(rules, sc):
    m = SessionMonitor(rules, sc["ceiling"], sc["hr_grade"])
    handlers = {
        "hr": lambda t, v: m.on_hr(t, v),
        "tick": lambda t, v: m.tick(t),
        "rpe": lambda t, v: m.on_rpe(t, v),
        "symptom": lambda t, v: m.on_symptom(t, v),
        "user_stop": lambda t, v: m.on_user_stop(t),
        "interaction": lambda t, v: m.on_interaction(t),
        "resume": lambda t, v: m.resume(t),
    }
    got = []
    for t, kind, v in expand_events(sc["events"]):
        got += [[a.t, a.kind.value, a.code] for a in handlers[kind](t, v)]
    expected = [[t, ActionKind(k).value, c] for t, k, c in sc["expected"]]
    return got == expected, got


# ---- 응급 흐름 ----
def run_emergency(rules, sc):
    fmt = lambda acts: [[a.value, c] for a, c in acts]
    flow = EmergencyFlow(rules, sc["start"]["t"], sc["start"]["severe"])
    trace = [fmt(flow.started)]
    ok = trace[0] == sc["start_expected"]
    for t, op, arg, expected in sc["steps"]:
        if op == "answer":
            acts = flow.answer(t, arg)
        else:
            acts = getattr(flow, op)(t)
        trace.append(fmt(acts))
        ok = ok and fmt(acts) == expected
    ok = ok and flow.state.value == sc["final"]
    return ok, {"trace": trace, "final": flow.state.value}


SUITES = {
    "precheck.csv": (read_csv, run_precheck_row),
    "hr_limits.csv": (read_csv, run_limits_row),
    "post_and_allowance.csv": (read_csv, run_misc_row),
    "session.yaml": (read_yaml, run_session),
    "emergency.yaml": (read_yaml, run_emergency),
}


def load_suite(name, directory=SCENARIO_DIR):
    reader, runner = SUITES[name]
    return reader(Path(directory) / name), runner
