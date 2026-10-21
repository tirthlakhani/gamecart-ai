
from datetime import datetime, timezone
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("GameCart AI")

# Demo catalogue: illustrative prices, not live market data.
PRODUCTS = [
    {
        "id": "G001",
        "name": "Cosmic Byte Gaming Headset",
        "category": "headset",
        "price": 2999,
        "currency": "INR",
        "features": ["over-ear", "microphone", "gaming"],
        "store": "Demo Store A",
    },
    {
        "id": "G002",
        "name": "RGB Mechanical Keyboard",
        "category": "keyboard",
        "price": 4599,
        "currency": "INR",
        "features": ["RGB", "mechanical keys", "gaming"],
        "store": "Demo Store B",
    },
    {
        "id": "G003",
        "name": "Wireless Gaming Controller",
        "category": "controller",
        "price": 3499,
        "currency": "INR",
        "features": ["wireless", "controller", "gaming"],
        "store": "Demo Store A",
    },
    {
        "id": "G004",
        "name": "Gaming Mouse",
        "category": "mouse",
        "price": 1499,
        "currency": "INR",
        "features": ["ergonomic", "USB", "gaming"],
        "store": "Demo Store C",
    },
    {
        "id": "G005",
        "name": "Gaming Headset Pro",
        "category": "headset",
        "price": 3899,
        "currency": "INR",
        "features": ["over-ear", "microphone", "wireless"],
        "store": "Demo Store B",
    },
]

wishlist = []


@mcp.tool()
def search_products(query: str = "") -> dict:
    """Search the demo gaming catalogue by product name, category, or feature."""
    words = query.lower().split()

    matches = [
        product for product in PRODUCTS
        if not words or any(
            word in (
                product["name"] + " " +
                product["category"] + " " +
                " ".join(product["features"])
            ).lower()
            for word in words
        )
    ]

    return {
        "count": len(matches),
        "note": "Illustrative demo catalogue; prices are not live.",
        "products": matches,
    }


@mcp.tool()
def compare_prices(product_query: str) -> dict:
    """Compare demo catalogue prices for matching gaming products."""
    query = product_query.lower().strip()

    matches = [
        product for product in PRODUCTS
        if query in product["name"].lower()
        or query in product["category"].lower()
    ]

    matches.sort(key=lambda product: product["price"])

    return {
        "count": len(matches),
        "currency": "INR",
        "note": "These are illustrative catalogue prices, not verified live offers.",
        "comparison": matches,
    }


@mcp.tool()
def filter_by_budget(max_budget: int, category: str = "") -> dict:
    """Find demo gaming products within a maximum budget in INR."""
    if max_budget < 0:
        return {"error": "Budget cannot be negative."}

    category = category.lower().strip()

    matches = [
        product for product in PRODUCTS
        if product["price"] <= max_budget
        and (
            not category
            or category in product["category"].lower()
        )
    ]

    matches.sort(key=lambda product: product["price"])

    return {
        "budget_inr": max_budget,
        "category": category or "all",
        "count": len(matches),
        "products": matches,
    }


@mcp.tool()
def manage_wishlist(
    action: str,
    product_id: str = "",
) -> dict:
    """Add, remove, or view wishlist items. Actions: add, remove, list."""
    action = action.lower().strip()

    if action == "list":
        return {"count": len(wishlist), "wishlist": wishlist}

    if action not in ("add", "remove"):
        return {"error": "Action must be add, remove, or list."}

    product = next(
        (p for p in PRODUCTS if p["id"] == product_id),
        None,
    )

    if not product:
        return {"error": "Product ID not found in the demo catalogue."}

    if action == "add":
        if any(p["id"] == product_id for p in wishlist):
            return {"message": "Product is already in the wishlist."}

        wishlist.append(product)
        return {
            "message": "Product added to wishlist.",
            "product": product,
        }

    wishlist[:] = [
        p for p in wishlist if p["id"] != product_id
    ]

    return {
        "message": "Product removed if it was present.",
        "wishlist_count": len(wishlist),
    }


@mcp.tool()
def get_store_summary() -> dict:
    """Get a summary of the demo catalogue and wishlist."""
    categories = sorted({p["category"] for p in PRODUCTS})

    return {
        "project": "GameCart AI",
        "catalogue_size": len(PRODUCTS),
        "categories": categories,
        "wishlist_count": len(wishlist),
        "price_currency": "INR",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "notice": "Demo data only; no live store integration.",
    }


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
