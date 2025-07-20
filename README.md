# 🛒 Ecommerce Backend API

FastAPI + MongoDB ecommerce backend built for HROne Backend Intern Task.

## 🔧 Tech Stack

- FastAPI (Python 3.10+)
- MongoDB (Atlas M0)
- Motor (Async MongoDB driver)
- Deployed on [Railway](https://railway.app)

---

## 📁 Features

- 🛍 Create and list products with filters
- 📦 Create orders and list by user
- 🔍 Regex + size filters on product list
- 🧮 Pagination with `next`, `limit`, `previous`
- 🔄 MongoDB joins for order product details

---

## 🧱 Project Structure

ecommerce-backend/
├── app/
│ ├── main.py
│ ├── database.py
│ ├── config.py
│ ├── routes/
│ │ └── api.py
│ └── schemas/
│ └── models.py
├── .env # DO NOT COMMIT
├── .gitignore
├── requirements.txt
└── README.md


---

## 🚀 API Endpoints

### ➕ POST `/products`
**Request**
```json
{
  "name": "T-Shirt",
  "price": 299.0,
  "sizes": [
    { "size": "small", "quantity": 10 }
  ]
}
```
### Response
```json
{ "id": "..." }
```

### 📄 GET /products

Supports query parameters: name, size, limit, offset

```json
{
  "data": [
    {
      "id": "123",
      "name": "T-Shirt",
      "price": 299.0
    }
  ],
  "page": {
    "next": "10",
    "limit": 2,
    "previous": 0
  }
}

```

### ➕ POST /orders

```json
{
  "userId": "user_1",
  "items": [
    { "productId": "64c123...", "qty": 2 }
  ]
}

```

### Response

```json
{ "id": "..." }
```

### 📄 GET /orders/{user_id}

### Response

```json

{
  "data": [
    {
      "id": "order123",
      "items": [
        {
          "id": "64c123...",
          "name": "T-Shirt",
          "qty": 2
        }
      ],
      "total": 598.0
    }
  ],
  "page": {
    "next": null,
    "limit": 1,
    "previous": 0
  }
}

```


- git clone https://github.com/YOUR_USERNAME/ecommerce-backend.git
- cd ecommerce-backend
- python -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt
- uvicorn app.main:app --reload
