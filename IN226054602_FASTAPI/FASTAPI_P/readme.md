# 🍕 FastAPI Food Delivery Backend System

## 🚀 Project Overview
This project is a fully functional backend system for a **Food Delivery Application** built using **FastAPI**. It simulates real-world backend operations such as menu management, order processing, cart handling, and advanced data querying.

The application is designed to demonstrate strong API development skills, clean code structuring, and implementation of real-world workflows.

---

## 🎯 Objectives
- Build RESTful APIs using FastAPI
- Implement CRUD operations
- Use Pydantic for request validation
- Design modular helper functions
- Handle multi-step workflows (Cart → Checkout → Orders)
- Implement advanced features like filtering, sorting, and pagination

---

## 🛠 Tech Stack
- **Python**
- **FastAPI**
- **Pydantic**
- **Uvicorn**

---

## 📂 Project Structure
## ⚙️ Features Implemented

### 🟢 1. Menu Management
- View all menu items
- Get item by ID
- Add new menu items
- Update item price and availability
- Delete menu items
- Menu summary (available/unavailable/categories)

---

### 🟡 2. Order System
- Place orders using validated request body
- Automatic bill calculation
- Delivery charge logic
- Order tracking with unique IDs
- View all orders

---

### 🟠 3. Cart System
- Add items to cart
- Update item quantity if already exists
- View cart with total price
- Remove item from cart
- Checkout system (multi-step workflow)
- Convert cart items into orders

---

### 🔵 4. Advanced APIs
- 🔍 Search menu (by name & category)
- 🔃 Sort menu (price, name, category)
- 📄 Pagination support
- 🎯 Filter menu (category, price, availability)
- 🚀 Combined endpoint (search + sort + pagination)

---

## 📌 API Endpoints

### 🟢 Basic Endpoints
| Method | Endpoint | Description |
|--------|---------|------------|
| GET | `/` | Welcome message |
| GET | `/menu` | Get all menu items |
| GET | `/menu/{item_id}` | Get item by ID |
| GET | `/menu/summary` | Menu statistics |
| GET | `/orders` | Get all orders |

---

### 🟡 Order Endpoints
| Method | Endpoint | Description |
|--------|---------|------------|
| POST | `/orders` | Place an order |
| GET | `/orders/search` | Search orders by customer |
| GET | `/orders/sort` | Sort orders by price |

---

### 🟠 Menu CRUD
| Method | Endpoint | Description |
|--------|---------|------------|
| POST | `/menu` | Add new item |
| PUT | `/menu/{item_id}` | Update item |
| DELETE | `/menu/{item_id}` | Delete item |

---

### 🔵 Cart Endpoints
| Method | Endpoint | Description |
|--------|---------|------------|
| POST | `/cart/add` | Add item to cart |
| GET | `/cart` | View cart |
| DELETE | `/cart/{item_id}` | Remove item |
| POST | `/cart/checkout` | Checkout cart |

---

### 🔴 Advanced Endpoints
| Method | Endpoint | Description |
|--------|---------|------------|
| GET | `/menu/filter` | Filter menu |
| GET | `/menu/search` | Search menu |
| GET | `/menu/sort` | Sort menu |
| GET | `/menu/page` | Pagination |
| GET | `/menu/browse` | Combined API |

---

## 🔍 Sample Request (Order)

```json
{
  "customer_name": "Rahul Sharma",
  "item_id": 1,
  "quantity": 2,
  "delivery_address": "123 MG Road, Bangalore, Karnataka",
  "order_type": "delivery"
}
