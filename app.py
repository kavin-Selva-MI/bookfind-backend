from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)  # This allows your HTML file to talk to this server

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
}

# ─────────────────────────────────────────────
#  One function per store
#  Each returns: { "store": "...", "url": "...", "price": "...", "found": True/False }
# ─────────────────────────────────────────────

def search_panuval(title):
    store = "Panuval"
    url = f"https://www.panuval.com/search?q={requests.utils.quote(title)}"
    try:
        res = requests.get(url, headers=HEADERS, timeout=8)
        soup = BeautifulSoup(res.text, "html.parser")
        # TODO: inspect panuval.com and update this selector
        <span class="price-normal">₹50</span>
        price = price_tag.get_text(strip=True) if price_tag else "Visit site to check"
        return {"store": store, "url": url, "price": price, "found": bool(price_tag)}
    except Exception as e:
        return {"store": store, "url": url, "price": "Could not reach site", "found": False}


def search_commonfolks(title):
    store = "Common Folks"
    url = f"https://www.commonfolksbookstore.com/search?q={requests.utils.quote(title)}"
    try:
        res = requests.get(url, headers=HEADERS, timeout=8)
        soup = BeautifulSoup(res.text, "html.parser")
        # TODO: inspect commonfolksbookstore.com and update this selector
        price_tag = soup.select_one(".price, .product-price, span.money")
        price = price_tag.get_text(strip=True) if price_tag else "Visit site to check"
        return {"store": store, "url": url, "price": price, "found": bool(price_tag)}
    except Exception as e:
        return {"store": store, "url": url, "price": "Could not reach site", "found": False}


def search_ethirveliyeedu(title):
    store = "Ethir Veliyeedu"
    url = f"https://ethirveliyeedu.com/?s={requests.utils.quote(title)}"
    try:
        res = requests.get(url, headers=HEADERS, timeout=8)
        soup = BeautifulSoup(res.text, "html.parser")
        # TODO: inspect ethirveliyeedu.com and update this selector
        price_tag = soup.select_one(".price, .woocommerce-Price-amount, ins .amount")
        price = price_tag.get_text(strip=True) if price_tag else "Visit site to check"
        return {"store": store, "url": url, "price": price, "found": bool(price_tag)}
    except Exception as e:
        return {"store": store, "url": url, "price": "Could not reach site", "found": False}


def search_zerodegree(title):
    store = "Zero Degree"
    url = f"https://zerodegreepublishing.com/?s={requests.utils.quote(title)}"
    try:
        res = requests.get(url, headers=HEADERS, timeout=8)
        soup = BeautifulSoup(res.text, "html.parser")
        # TODO: inspect zerodegreepublishing.com and update this selector
        price_tag = soup.select_one(".price, .woocommerce-Price-amount, ins .amount")
        price = price_tag.get_text(strip=True) if price_tag else "Visit site to check"
        return {"store": store, "url": url, "price": price, "found": bool(price_tag)}
    except Exception as e:
        return {"store": store, "url": url, "price": "Could not reach site", "found": False}


def search_vishnupuram(title):
    store = "Vishnupuram"
    url = f"https://www.vishnupuram.com/search?q={requests.utils.quote(title)}"
    try:
        res = requests.get(url, headers=HEADERS, timeout=8)
        soup = BeautifulSoup(res.text, "html.parser")
        # TODO: inspect vishnupuram.com and update this selector
        price_tag = soup.select_one(".price, .product-price, span.money")
        price = price_tag.get_text(strip=True) if price_tag else "Visit site to check"
        return {"store": store, "url": url, "price": price, "found": bool(price_tag)}
    except Exception as e:
        return {"store": store, "url": url, "price": "Could not reach site", "found": False}


# ─────────────────────────────────────────────
#  Main search endpoint
#  Your HTML app calls: GET /search?title=atomic+habits
# ─────────────────────────────────────────────

@app.route("/search")
def search():
    title = request.args.get("title", "").strip()
    if not title:
        return jsonify({"error": "No title provided"}), 400

    results = [
        search_panuval(title),
        search_commonfolks(title),
        search_ethirveliyeedu(title),
        search_zerodegree(title),
        search_vishnupuram(title),
    ]

    return jsonify({"title": title, "results": results})


@app.route("/")
def home():
    return "BookFind backend is running ✓"


if __name__ == "__main__":
    app.run(debug=True)
