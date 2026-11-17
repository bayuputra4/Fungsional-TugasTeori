"""Demo application: calculate and rank student grades."""

from fplib import compose, filter_items, group_by, map_items, pipe, sort_by, sum_by, unique_by


def build_summary(students: list[dict]) -> dict:
    normalize = compose(str.title, str.strip)
    eligible = filter_items(students, lambda student: len(student["scores"]) > 0)
    graded = map_items(
        eligible,
        lambda student: {
            **student,
            "name": normalize(student["name"]),
            "final": round(sum(student["scores"]) / len(student["scores"]), 2),
        },
    )
    by_class = group_by(graded, lambda student: student["class"])
    classes = map_items(
        unique_by(graded, lambda student: student["class"]),
        lambda student: student["class"],
    )
    ranked = sort_by(graded, lambda student: student["final"], reverse=True)
    average = pipe(
        sum_by(graded, lambda student: student["final"]),
        lambda total: round(total / len(graded), 2) if graded else 0,
    )
    return {
        "ranked": ranked,
        "by_class": by_class,
        "classes": classes,
        "average": average,
    }


def main() -> None:
    students = [
        {"name": "  ayu putri", "class": "IF-A", "scores": [88, 92, 90]},
        {"name": "bima santoso", "class": "IF-A", "scores": [76, 80, 84]},
        {"name": "citra lestari", "class": "IF-B", "scores": [95, 91, 94]},
    ]
    summary = build_summary(students)
    print("=== Nilai Mahasiswa ===")
    for position, student in enumerate(summary["ranked"], start=1):
        print(f"{position}. {student['name']}: {student['final']}")
    print(f"Rata-rata kelas: {summary['average']}")


if __name__ == "__main__":
    main()
