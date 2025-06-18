# identity-recon service

This is a FastAPI-based web service to identify and consolidate customer contacts based on their email and/or phone number. It maintains linked contacts with primary and secondary precedence.

---

## Features

- Create and consolidate contacts by email or phone number.
- Link contacts sharing common email or phone number.
- Automatically manage primary and secondary contacts.
- Returns consolidated contact info including all emails, phone numbers, and linked contact IDs.

---

## Requirements

- Python 3.9+
- SQLite (default database)
- `pip` package manager

---

## Setup & Installation


git clone <repo-url>
cd <repo-directory>

python -m venv venv

source venv/bin/activate #MacOS/Linux

venv\Scripts\activate     # Windows

pip install -r requirements.txt

uvicorn app.main:app --reload

