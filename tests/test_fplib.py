import pytest

from fplib import compose, filter_items, group_by, map_items, pipe, sort_by, sum_by, unique_by


def test_pipe_runs_functions_from_left_to_right():
    assert pipe(3, lambda value: value + 2, lambda value: value * 4) == 20
    assert pipe(3) == 3


def test_compose_runs_functions_from_right_to_left():
    normalize = compose(str.title, str.strip)
    assert normalize("  fungsional ") == "Fungsional"
    assert compose()(7) == 7


def test_map_and_filter_return_new_lists():
    source = [1, 2, 3, 4]
    assert map_items(source, lambda value: value * 2) == [2, 4, 6, 8]
    assert filter_items(source, lambda value: value % 2 == 0) == [2, 4]
    assert source == [1, 2, 3, 4]


def test_sum_by_and_group_by():
    records = [{"team": "A", "score": 4}, {"team": "B", "score": 7}, {"team": "A", "score": 3}]
    assert sum_by(records, lambda record: record["score"]) == 14
    assert group_by(records, lambda record: record["team"]) == {
        "A": [records[0], records[2]],
        "B": [records[1]],
    }


def test_unique_by_preserves_first_item_and_sort_by_is_non_mutating():
    records = [{"id": 2}, {"id": 1}, {"id": 2}]
    assert unique_by(records, lambda record: record["id"]) == records[:2]
    assert sort_by(records, lambda record: record["id"]) == [records[1], records[0], records[2]]
    assert [record["id"] for record in records] == [2, 1, 2]


@pytest.mark.parametrize(
    ("builder", "arguments", "expected"),
    [
        ("kasir_kantin", "build_summary", 28000),
        ("presensi_kelas", "build_summary", 66.7),
        ("perpustakaan_mini", "build_summary", 2000),
        ("keuangan_pribadi", "build_summary", 1445000),
        ("nilai_mahasiswa", "build_summary", 87.78),
    ],
)
def test_demo_applications(builder, arguments, expected):
    module = __import__(builder)
    build_summary = getattr(module, arguments)
    if builder == "kasir_kantin":
        result = build_summary([], [{"price": 14000, "quantity": 2}])
        assert result["total"] == expected
    elif builder == "presensi_kelas":
        result = build_summary([{"name": "ayu", "class": "IF-A", "status": "Hadir"},
                                {"name": "bima", "class": "IF-A", "status": "Izin"},
                                {"name": "citra", "class": "IF-B", "status": "Hadir"}])
        assert result["attendance_rate"] == expected
        assert result["present"][0]["name"] == "Ayu"
    elif builder == "perpustakaan_mini":
        result = build_summary([], [{"fine": 2000}])
        assert result["total_fines"] == expected
    elif builder == "keuangan_pribadi":
        result = build_summary([{"date": "2026-01-01", "kind": "Pemasukan", "category": "lain", "amount": 1500000},
                                {"date": "2026-01-02", "kind": "Pengeluaran", "category": "lain", "amount": 55000}])
        assert result["balance"] == expected
        assert "Lain" in result["expenses_by_category"]
    else:
        result = build_summary([{"name": "ayu", "class": "IF-A", "scores": [88, 92, 90]},
                                {"name": "bima", "class": "IF-A", "scores": [76, 80, 84]},
                                {"name": "citra", "class": "IF-B", "scores": [95, 91, 94]}])
        assert result["average"] == expected
