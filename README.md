# digiWallet
Affinsys [assignment](https://gist.github.com/ashu-affinsys/c15a16b73f8e88c3f87c60ec994e31fd) to simulate a digital wallet system.  
  
This is a backend-only RESTful API that simulates a **digital wallet** system. It allows users to register, fund their account, pay other users, view transaction history, and purchase products using wallet balance.

> Built with Python, FastAPI, SQLAlchemy, and PostgreSQL.

---

## 🚀 Features

- ✅ User registration with hashed passwords (`bcrypt`)
- ✅ Basic Authentication for protected routes
- ✅ Fund account (deposit money)
- ✅ Pay other users
- ✅ Check balance (with optional currency conversion)
- ✅ View transaction history
- ✅ Add and list products
- ✅ Buy products using wallet balance
- 🔐 All protected routes use HTTP Basic Auth

---

## 📦 Project Structure

```
wallet/
├── main.py          # FastAPI route definitions
├── models.py        # SQLAlchemy models (User, Transaction, Product)
├── database.py      # DB connection setup
├── schemas.py       # Pydantic request schemas
├── auth.py          # Password hashing and auth helpers
├── .env             # Environment variables (DB URL)
```

---

## ⚙️ Tech Stack

- Python 3.10+
- FastAPI
- PostgreSQL
- SQLAlchemy
- bcrypt (via passlib)
- currencyapi.com (for currency conversion)

---

## 📥 Installation & Setup

### 1. Clone the Repository:  
  
```bash
git clone https://github.com/ejdotp/digiWallet
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```
### OR

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary passlib[bcrypt] python-dotenv requests
```

### 3. Set Up PostgreSQL

Make sure PostgreSQL is installed and running.

Create a database:

```sql
CREATE DATABASE wallet_db;
```

### 4. Create a `.env` File

```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/wallet_db
```

Change the `yourpassword` accordingly.

---

## ▶️ Run the App

```bash
python -m uvicorn main:app --reload
```

Visit the docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🔐 Authentication

Use **Basic Auth** for all protected routes:

```
Authorization: Basic base64(username:password)
```

You can test this easily in Swagger docs under "Authorize".

---

## 🧪 Example API Calls (cURL)

### ✅ Register

```bash
curl -X POST http://127.0.0.1:8000/register \
 -H "Content-Type: application/json" \
 -d '{"username": "ashu", "password": "hunter2"}'
```

### 💰 Fund Wallet

```bash
curl -X POST http://127.0.0.1:8000/fund \
 -u ashu:hunter2 \
 -H "Content-Type: application/json" \
 -d '{"amt": 10000}'
```

---

## 📚 API Endpoints

| Method | Endpoint       | Auth | Description                     |
|--------|----------------|------|---------------------------------|
| POST   | `/register`    | ❌    | Create new user                 |
| POST   | `/fund`        | ✅    | Deposit money into wallet       |
| POST   | `/pay`         | ✅    | Pay another user                |
| GET    | `/bal`         | ✅    | Get balance (optionally in USD) |
| GET    | `/stmt`        | ✅    | View transaction history        |
| POST   | `/product`     | ✅    | Add a product                   |
| GET    | `/product`     | ❌    | List all products               |
| POST   | `/buy`         | ✅    | Buy a product                   |

---

## 🌍 Currency Conversion

To get balance in other currencies (e.g., USD):

```
GET /bal?currency=USD
```

Uses [currencyapi.com](https://currencyapi.com). You'll need to register for a free API key and add this to your request logic.

---

## 📌 Notes

- No frontend is included.
- No Dockerfile yet, but easily dockerizable.
- No admin roles or authorization logic (optional future upgrade).

