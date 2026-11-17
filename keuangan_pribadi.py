"""Demo application: a simple personal finance recap."""

from fplib import compose, filter_items, group_by, map_items, pipe, sort_by, sum_by, unique_by


def build_summary(transactions: list[dict]) -> dict:
    normalize = compose(str.title, str.strip)
    clean_transactions = map_items(
        transactions,
        lambda item: {**item, "category": normalize(item["category"])},
    )
    expenses = filter_items(clean_transactions, lambda item: item["kind"] == "Pengeluaran")
    by_category = group_by(expenses, lambda item: item["category"])
    categories = map_items(
        unique_by(clean_transactions, lambda item: item["category"]),
        lambda item: item["category"],
    )
    timeline = sort_by(clean_transactions, lambda item: item["date"])
    balance = pipe(
        sum_by(
            transactions,
            lambda item: item["amount"] if item["kind"] == "Pemasukan" else -item["amount"],
        ),
        lambda amount: round(amount, 2),
    )
    return {
        "timeline": timeline,
        "expenses_by_category": by_category,
        "categories": categories,
        "balance": balance,
    }


def main() -> None:
    transactions = [
        {"date": "2026-11-02", "kind": "Pemasukan", "category": "  beasiswa", "amount": 1500000},
        {"date": "2026-11-03", "kind": "Pengeluaran", "category": "makan", "amount": 35000},
        {"date": "2026-11-04", "kind": "Pengeluaran", "category": "makan", "amount": 20000},
    ]
    summary = build_summary(transactions)
    print("=== Keuangan Pribadi ===")
    print(f"Saldo bersih: Rp{summary['balance']:,}")
    print(f"Kategori: {', '.join(summary['categories'])}")
    print(f"Pengeluaran: {', '.join(summary['expenses_by_category'])}")


if __name__ == "__main__":
    main()
