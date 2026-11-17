"""Demo application: a mini library catalog and fine recap."""

from fplib import compose, filter_items, group_by, map_items, pipe, sort_by, sum_by, unique_by


def build_summary(books: list[dict], loans: list[dict]) -> dict:
    normalize = compose(str.title, str.strip)
    available = filter_items(books, lambda book: book["available"])
    clean_books = map_items(
        available,
        lambda book: {**book, "title": normalize(book["title"])},
    )
    by_category = group_by(clean_books, lambda book: book["category"])
    categories = map_items(
        unique_by(clean_books, lambda book: book["category"]),
        lambda book: book["category"],
    )
    catalog = sort_by(clean_books, lambda book: book["title"].casefold())
    total_fines = pipe(
        sum_by(loans, lambda loan: loan["fine"]),
        lambda amount: round(amount, 2),
    )
    return {
        "catalog": catalog,
        "by_category": by_category,
        "categories": categories,
        "total_fines": total_fines,
    }


def main() -> None:
    books = [
        {"title": "  bumi manusia", "category": "Novel", "available": True},
        {"title": "algoritma dasar", "category": "Pendidikan", "available": True},
        {"title": "laut bercerita", "category": "Novel", "available": False},
    ]
    loans = [{"borrower": "Ayu", "fine": 2000}, {"borrower": "Bima", "fine": 0}]
    summary = build_summary(books, loans)
    print("=== Perpustakaan Mini ===")
    print(f"Katalog tersedia: {', '.join(book['title'] for book in summary['catalog'])}")
    print(f"Kategori: {', '.join(summary['categories'])}")
    print(f"Total denda: Rp{summary['total_fines']:,}")


if __name__ == "__main__":
    main()
