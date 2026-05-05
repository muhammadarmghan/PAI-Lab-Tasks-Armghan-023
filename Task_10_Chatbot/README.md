# Task 11 — Restaurant Information Bot

Simple Flask-based chatbot demo that answers basic restaurant queries:
- Menu
- Reservation availability
- Order tracking (by order number)

Run locally:

```powershell
cd Task_11_Chatbot
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser.

API: POST `/api/query` JSON {"query": "show menu"}
