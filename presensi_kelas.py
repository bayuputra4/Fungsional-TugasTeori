"""Demo application: attendance recap for a class."""

from fplib import compose, filter_items, group_by, map_items, pipe, sort_by, sum_by, unique_by


def build_summary(records: list[dict]) -> dict:
    normalize = compose(str.title, str.strip)
    clean_records = map_items(
        records,
        lambda record: {**record, "name": normalize(record["name"])},
    )
    present = filter_items(clean_records, lambda record: record["status"] == "Hadir")
    by_class = group_by(clean_records, lambda record: record["class"])
    classes = map_items(
        unique_by(clean_records, lambda record: record["class"]),
        lambda record: record["class"],
    )
    ranked = sort_by(present, lambda record: record["name"].casefold())
    attendance_rate = pipe(
        sum_by(present, lambda _record: 1),
        lambda count: round(count / len(records) * 100, 1) if records else 0,
    )
    return {
        "present": ranked,
        "by_class": by_class,
        "classes": classes,
        "attendance_rate": attendance_rate,
    }


def main() -> None:
    records = [
        {"name": "  ayu putri", "class": "IF-A", "status": "Hadir"},
        {"name": "bima santoso", "class": "IF-A", "status": "Izin"},
        {"name": "citra lestari", "class": "IF-B", "status": "Hadir"},
    ]
    summary = build_summary(records)
    print("=== Presensi Kelas ===")
    print(f"Hadir: {', '.join(record['name'] for record in summary['present'])}")
    print(f"Kelas: {', '.join(summary['classes'])}")
    print(f"Persentase kehadiran: {summary['attendance_rate']}%")


if __name__ == "__main__":
    main()
