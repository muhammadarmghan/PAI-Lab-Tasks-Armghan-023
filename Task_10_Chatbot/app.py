from flask import Flask, render_template, request, jsonify
import re
from pathlib import Path

app = Flask(__name__, template_folder='templates', static_folder='static')

# Simple in-memory data for the demo
MENU = [
    {"name": "Margherita Pizza", "price": "$8.99"},
    {"name": "Pepperoni Pizza", "price": "$9.99"},
    {"name": "Caesar Salad", "price": "$6.50"},
    {"name": "Spaghetti Bolognese", "price": "$11.00"},
    {"name": "Tiramisu", "price": "$5.00"},
]

RESERVATION_SLOTS = {
    "available": 5,
    "next_available": "Today 7:30 PM"
}

ORDERS = {
    "1001": "Preparing",
    "1002": "Out for delivery",
    "1003": "Delivered"
}


def handle_query(query: str) -> dict:
    q = query.lower()
    if "menu" in q or "what" in q and "serve" in q:
        return {"intent": "menu", "menu": MENU}

    if any(k in q for k in ("reserve", "reservation", "book", "table")):
        return {
            "intent": "reservation",
            "available": RESERVATION_SLOTS["available"],
            "next_available": RESERVATION_SLOTS["next_available"],
        }

    if any(k in q for k in ("order", "track", "status")):
        # try to extract order number
        m = re.search(r"#?(\d{3,6})", q)
        if m:
            order_no = m.group(1)
            status = ORDERS.get(order_no, "Order not found")
            return {"intent": "order", "order_no": order_no, "status": status}
        return {"intent": "order", "message": "Please provide your order number (e.g. 1001)."}

    # fallback/help
    return {
        "intent": "fallback",
        "message": (
            "I can show the menu, reservation availability, or track orders. "
            "Try: 'show menu', 'reservation', or 'track order 1001'."
        ),
    }


@app.get('/')
def index():
    return render_template('index.html')


@app.post('/api/query')
def api_query():
    data = request.get_json(force=True, silent=True) or {}
    query = data.get('query') or data.get('q')
    if not query:
        return jsonify({"error": "missing 'query' in JSON body"}), 400
    resp = handle_query(query)
    return jsonify(resp)


if __name__ == '__main__':
    app.run(debug=True)
