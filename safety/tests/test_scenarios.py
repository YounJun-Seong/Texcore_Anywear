"""정답표 전체 재생. 하나라도 어긋나면 실패(납품 검수 기준 98%보다 엄격하게 100%를 유지)."""
import pytest

from scenario_runner import SUITES, load_suite


def _cases():
    for name in SUITES:
        rows, runner = load_suite(name)
        for row in rows:
            yield pytest.param(runner, row, id=f"{row['id']}")


@pytest.mark.parametrize("runner,row", list(_cases()))
def test_scenario(rules, runner, row):
    ok, got = runner(rules, row)
    assert ok, f"{row['id']} {row.get('note') or row.get('desc')}: expected {row.get('expected')}, got {got}"


def test_scenario_count_meets_contract():
    total = sum(len(load_suite(name)[0]) for name in SUITES)
    assert total >= 300, total


def test_ids_unique():
    ids = [row["id"] for name in SUITES for row in load_suite(name)[0]]
    assert len(ids) == len(set(ids))
