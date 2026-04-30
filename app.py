from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; BookFindBot/1.0)"
}

TIMEOUT = 10


# ---------- PANUVAL ----------
def search_panuval(title: str):
    search_url = "https://www.panuval.com/search"
    params = {"q": title}

    try:
        response = requests.get(
            search_url,
            params=params,
            headers=HEADERS,
            timeout=TIMEOUT
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        book_card = soup.select_one("div.product-item")

        if not book_card:
            return {
                "store": "Panuval",
                "price": "Not found",
                "availability": "Not available",
                "url": search_url
            }

        # ✅ EXACT PRICE SELECTOR FROM HTML
        price_tag = book_card.select_one("span.price-normal")
        price = price_tag.get_text(strip=True) if price_tag else "Check site"

        link_tag = book_card.find("a", href=True)
        book_url = (
            "https://www.panuval.com" + link_tag["href"]
            if link_tag else search_url
        )

        return {
            "store": "Panuval",
            "price": price,
            "availability": "Available",
            "url": book_url
        }

    except Exception as e:
        print(f"[PANUVAL ERROR] {e}")
        return {
            "store": "Panuval",
            "price": "Error",
            "availability": "Unavailable",
            "url": search_url
        }


# ---------- ANOTHER SITE (EXAMPLE) ----------
def search_other_store(title: str):
    """
    Example second bookstore.
    Update selectors based on actual site HTML.
    """

    search_url = "https://examplebookstore.com/search"
    params = {"q": title}

    try:
        response = requests.get(
            search_url,
            params=params,
            headers=HEADERS,
            timeout=TIMEOUT
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        book_card = soup.select_one("div.book-item")

        if not book_card:
            return {
                "store": "OtherStore",
                "price": "Not found",
                "availability": "Not available",
                "url": search_url
            }

        price_tag = book_card.select_one(".price")
        price = price_tag.get_text(strip=True) if price_tag else "Check site"

        link_tag = book_card.find("a", href=True)
        book_url = link_tag["href"] if link_tag else search_url

        return {
            "store": "OtherStore",
            "price": price,
            "availability": "Available",
            "url": book_url
        }

    except Exception as e:
        print(f"[OTHER STORE ERROR] {e}")
        return {
            "store": "OtherStore",
            "price": "Error",
            "availability": "Unavailable",
            "url": search_url
        }


# ---------- API ROUTE ----------
@app.route("/search", methods=["GET"])
def search_books():
    title = request.args.get("title")

    if not title:
        return jsonify({
            "success": False,
            "error": "Query parameter 'title' is required"
        }), 400

    results = []

    results.append(search_panuval(title))
    results.append(search_other_store(title))

    return jsonify({
        "success": True,
        "query": title,
        "results": results
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
``
