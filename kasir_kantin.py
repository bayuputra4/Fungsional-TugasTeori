"""Demo application: a small canteen checkout summary."""

from fplib import compose, filter_items, group_by, map_items, pipe, sort_by, sum_by, unique_by


def build_summary(products: list[dict], cart: list[dict]) -> dict:
    normalize = compose(str.title, str.strip)
    available = filter_items(products, lambda product: product["stock"] > 0)
    display_products = map_items(
        available,
        lambda product: {**product, "name": normalize(product["name"])},
    )
    categories = group_by(display_products, lambda product: product["category"])
    category_names = map_items(
        unique_by(display_products, lambda product: product["category"]),
        lambda product: product["category"],
    )
    sorted_products = sort_by(display_products, lambda product: product["price"])
    total = pipe(
        sum_by(cart, lambda item: item["price"] * item["quantity"]),
        lambda amount: round(amount, 2),
    )
    return {
        "available_products": sorted_products,
        "categories": categories,
        "category_names": category_names,
        "total": total,
    }


def main() -> None:
    products = [
        {"name": "  nasi goreng", "category": "Makanan", "price": 12000, "stock": 8},
        {"name": "es teh", "category": "Minuman", "price": 4000, "stock": 12},
        {"name": "roti bakar", "category": "Makanan", "price": 9000, "stock": 0},
    ]
    cart = [
        {"name": "Nasi Goreng", "price": 12000, "quantity": 2},
        {"name": "Es Teh", "price": 4000, "quantity": 1},
    ]
    summary = build_summary(products, cart)
    print("=== Kasir Kantin ===")
    print(f"Menu tersedia: {', '.join(item['name'] for item in summary['available_products'])}")
    print(f"Kategori: {', '.join(summary['category_names'])}")
    print(f"Total belanja: Rp{summary['total']:,}")


if __name__ == "__main__":
    main()
