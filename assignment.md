# 🧪 API Design & Implementation Exercise

Welcome! In this assignment, you'll be building a backend service that simulates a **digital wallet system** with the ability to fund your account, pay other users, view transaction history, and even purchase products. The goal is to help you understand REST API design, authentication, external API integration, and best practices around security and error handling.

This is a **hands-on, backend-only** assignment — you will **not** build any front-end or UI. Focus on writing clean, readable, and testable code.

---

## 🎯 Objectives

By completing this exercise, you will:

- Implement basic user authentication with hashed passwords
- Understand and implement **Basic Authentication**
- Learn to **secure APIs** and validate inputs
- Design and implement APIs for **fund transfers and transactions**
- Integrate with a **real external API** for currency conversion
- Add a **product purchase workflow** using wallet balance
- Use appropriate **HTTP methods and status codes**
- Handle edge cases with clear and consistent error responses
- Follow **JSON-based API response standards**

---

> **Make sure to commit your changes to a public github repository**
> Feel free to deploy your project on platforms like  `vercel` etc

## 🧰 What You’ll Build

You will build the following features:

- ✅ User registration with password hashing
- ✅ Basic Authentication for protected endpoints
- ✅ Fund account (deposit money)
- ✅ Pay another user
- ✅ Check your balance (optionally in another currency)
- ✅ See your transaction history
- ✅ Add products to a global catalog
- ✅ Buy products using wallet balance

You can use **any programming language** or framework you are comfortable with. Bonus points if your code is modular and well-tested.

## Constraints
> Use any relation database, `postgres`, `mysql`, `sqlite` or cloud providers like `supabase`, `neon`, `rds` etc

> The data mus be persistent, **DO NOT USE IN MEMORY VARIABLES AS YOUR DATABASE**
> The data mus be stuctured, **DO NOT USE IN FREE FORM NO-SQL DB's like mongodb** You can use structured nosql like `dynamo`, `scylla`, `cassandra` if you need to


> Feel free to use tools like `redis` for caching/ queuing functionality if you need to

---

## 🔐 Authentication

All protected routes must use **Basic Auth**. This means that every request should send the following HTTP header:

```
Authorization: Basic <base64(username:password)>
```

> 🔒 Store passwords using a strong hashing algorithm like **bcrypt**.

---

## 🌍 External API

To convert wallet balance (which is stored in **INR**) into other currencies, use this public exchange rate API:

- 🌐 [https://currencyapi.com](https://currencyapi.com)

Example: If a user requests their balance in USD, your API should fetch the latest INR→USD rate and return the converted balance.

---

## 📦 API Requirements

Below are the APIs you must implement. You can extend them if needed but should implement all the listed behavior.

---

### 1. Register User  
Create a new user account.

**Endpoint:** `POST /register`  
**Authentication:** ❌ No auth required  
**Request Body:**

```json
{
  "username": "ashu",
  "password": "hunter2"
}
```

**Response:**  
Status: `201 Created` if successful.

---

### 2. Fund Account  
Deposit money into the logged-in user's wallet.

**Endpoint:** `POST /fund`  
**Authentication:** ✅ Required  
**Headers:**

```
Authorization: Basic <base64(username:password)>
```

**Request Body:**
```json
{
  "amt": 10000
}
```

**Success Response:**
```json
{
  "balance": 10000
}
```

---

### 3. Pay Another User  
Transfer money from the logged-in user to another user.

**Endpoint:** `POST /pay`  
**Authentication:** ✅ Required  
**Request Body:**

```json
{
  "to": "priya",
  "amt": 100
}
```

**Success Response:**
```json
{
  "balance": 9900
}
```

**Failure Response:**  
Status: `400 Bad Request`  
Reason: insufficient funds or recipient doesn’t exist.

---

### 4. Check Balance (with optional currency)  
Retrieve wallet balance, optionally converted to another currency (e.g., USD, EUR).

**Endpoint:** `GET /bal?currency=USD`  
**Authentication:** ✅ Required  

**Success Response:**
```json
{
  "balance": 120.35,
  "currency": "USD"
}
```

> Use https://currencyapi.com for currency conversion rates.

---

### 5. View Transaction History  
Return a list of all the user’s transactions in reverse chronological order.

**Endpoint:** `GET /stmt`  
**Authentication:** ✅ Required

**Response:**
```json
[
  { "kind": "debit", "amt": 100, "updated_bal": 9900, "timestamp": "2025-06-09T10:00:00Z" },
  { "kind": "credit", "amt": 10000, "updated_bal": 10000, "timestamp": "2025-06-09T09:00:00Z" }
]
```

---

### 6. Add Product  
Admins or logged-in users can add products to a global catalog. Each product includes name, price (in INR), and a short description.

**Endpoint:** `POST /product`  
**Authentication:** ✅ Required

**Request Body:**
```json
{
  "name": "Wireless Mouse",
  "price": 599,
  "description": "2.4 GHz wireless mouse with USB receiver"
}
```

**Response:**  
Status: `201 Created`
```json
{
  "id": 1,
  "message": "Product added"
}
```

---

### 7. List All Products  
List all available products in the catalog.

**Endpoint:** `GET /product`  
**Authentication:** ❌ Not required

**Response:**
```json
[
  {
    "id": 1,
    "name": "Wireless Mouse",
    "price": 599,
    "description": "2.4 GHz wireless mouse with USB receiver"
  }
]
```

---

### 8. Buy a Product  
Use wallet balance to purchase a product. The price should be deducted from the user’s balance and a transaction should be recorded.

**Endpoint:** `POST /buy`  
**Authentication:** ✅ Required

**Request Body:**
```json
{
  "product_id": 1
}
```

**Success Response:**
```json
{
  "message": "Product purchased",
  "balance": 9301
}
```

**Failure Response:**
Status: `400 Bad Request`
```json
{
  "error": "Insufficient balance or invalid product"
}
```

---

## 🧪 Additional Notes

- Use in-memory storage (like dictionaries or maps) for a quick prototype, or a real database if you want to go further.
- Each API should respond in clean and consistent **JSON** format.
- Focus on **correctness**, **readability**, and **error handling**.
- Feel free to write tests, comments, or sample curl commands.

Happy coding! 🚀