"""컴파일된 engine.js(Dart → JS)를 브라우저에서 돌려 정답표 352건과 맞춰 본다.

JS에는 정수·실수 구분이 없어 Dart VM과 결과가 달라질 수 있으므로, 데모에 넣기 전에 반드시 통과해야 한다.
    LD_LIBRARY_PATH=... ../.venv/bin/python demo/tests/engine_parity.py
"""
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "safety"))
sys.path.insert(0, str(ROOT / "safety" / "tools"))
from safety_engine import load_rules  # noqa: E402
from scenario_runner import _num, _set, expand_events, read_csv, read_yaml  # noqa: E402

SC = ROOT / "safety" / "scenarios"


def main():
    rules = load_rules()
    cases = []
    for row in read_csv(SC / "precheck.csv"):
        limits = {k: _num(row[c]) for k, c in [("systolic_max", "dr_sbp_max"), ("diastolic_max", "dr_dbp_max"),
                                               ("resting_hr_max", "dr_hr_max"), ("exercise_hr_ceiling", "dr_hr_ceiling")]}
        cases.append({"kind": "pre", "id": row["id"], "expected": row["expected"],
                      "codes": sorted(_set(row["expected_codes"])),
                      "arg": {"profile": {"age": int(row["age"]), "conditions": sorted(_set(row["gate_conditions"])),
                                          "parq_risk": row["parq_risk"] == "1", "doctor_clearance": row["clearance"] == "1",
                                          "device": row["device"] or None,
                                          "doctor_limits": {k: v for k, v in limits.items() if v is not None}},
                              "vitals": {"systolic": _num(row["sbp"]), "diastolic": _num(row["dbp"]),
                                         "resting_hr": _num(row["hr"]), "bp_source": row["bp_source"],
                                         "hr_source": row["hr_source"]},
                              "symptoms": sorted(_set(row["symptoms"])), "conditions": sorted(_set(row["conditions"]))}})
    for row in read_csv(SC / "hr_limits.csv"):
        cases.append({"kind": "lim", "id": row["id"], "expected": [int(row["expected_ceiling"]), row["expected_mode"]],
                      "arg": {"profile": {"age": int(row["age"]), "beta_blocker": row["beta_blocker"] == "1",
                                          "device": row["device"] or None,
                                          "doctor_limits": {"exercise_hr_ceiling": _num(row["dr_hr_ceiling"])}
                                          if row["dr_hr_ceiling"] else {}},
                              "weeks": int(row["weeks"]), "escalation": row["escalation"] == "1", "light": row["light"]}})
    for row in read_csv(SC / "post_and_allowance.csv"):
        if row["kind"] == "post_check":
            cases.append({"kind": "post", "id": row["id"], "expected": row["expected"],
                          "arg": {"resting_hr": int(row["a"]), "hr_after_recovery": int(row["b"])}})
        else:
            cases.append({"kind": "allow", "id": row["id"], "expected": int(row["expected"]),
                          "arg": {"light": row["a"], "minutes": int(row["b"])}})
    for sc in read_yaml(SC / "session.yaml"):
        cases.append({"kind": "session", "id": sc["id"], "ceiling": sc["ceiling"], "grade": sc["hr_grade"],
                      "events": expand_events(sc["events"]), "expected": sc["expected"]})
    for sc in read_yaml(SC / "emergency.yaml"):
        cases.append({"kind": "em", "id": sc["id"], "sc": sc})

    js = """([bundle, cases]) => {
      const E = window.SafetyEngine;
      const call = (f, a) => { const r = JSON.parse(E[f](JSON.stringify(a))); if (!r.ok) throw new Error(f + ': ' + r.error); return r.result; };
      call('load', {bundle});
      const fails = [];
      for (const c of cases) {
        try {
          let got, ok;
          if (c.kind === 'pre') {
            const d = call('preCheck', c.arg);
            ok = d.outcome === c.expected && c.codes.every(x => d.reasons.includes(x)); got = d;
          } else if (c.kind === 'lim') {
            const l = call('hrLimits', c.arg); got = [l.ceiling, l.mode]; ok = JSON.stringify(got) === JSON.stringify(c.expected);
          } else if (c.kind === 'post') {
            got = call('postCheck', c.arg).outcome; ok = got === c.expected;
          } else if (c.kind === 'allow') {
            got = call('allowance', c.arg).max_minutes; ok = got === c.expected;
          } else if (c.kind === 'session') {
            const id = call('monitorNew', {ceiling: c.ceiling, hr_grade: c.grade}).id;
            got = [];
            for (const [t, kind, v] of c.events) {
              const ev = {tick: 'tick', hr: 'hr', rpe: 'rpe', symptom: 'symptom', user_stop: 'user_stop', interaction: 'interaction', resume: 'resume'}[kind];
              for (const a of call('monitorEvent', {id, event: ev, t, value: v}).actions) got.push([a.t, a.kind, a.code]);
            }
            ok = JSON.stringify(got) === JSON.stringify(c.expected);
          } else {
            const s = c.sc;
            const f = call('flowNew', {t: s.start.t, severe: s.start.severe});
            ok = JSON.stringify(f.actions) === JSON.stringify(s.start_expected); got = [f.actions]; let state = f.state;
            for (const [t, op, arg, exp] of s.steps) {
              const r = call('flowEvent', {id: f.id, op, t, ok: arg === true});
              got.push(r.actions); state = r.state; ok = ok && JSON.stringify(r.actions) === JSON.stringify(exp);
            }
            ok = ok && state === s.final;
          }
          if (!ok) fails.push([c.id, JSON.stringify(got).slice(0, 200)]);
        } catch (e) { fails.push([c.id, String(e)]); }
      }
      return {total: cases.length, fails};
    }"""
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.set_content("<!doctype html><meta charset=utf-8><body></body>")
        pg.add_script_tag(path=str(ROOT / "demo" / "engine.js"))
        res = pg.evaluate(js, [rules.data, cases])
        b.close()
    print(f"engine.js 정답표 {res['total'] - len(res['fails'])}/{res['total']} 일치")
    for f in res["fails"][:20]:
        print("  ✗", f)
    if errors:
        print("page errors:", errors)
    sys.exit(1 if res["fails"] or errors or res["total"] < 352 else 0)


if __name__ == "__main__":
    main()
