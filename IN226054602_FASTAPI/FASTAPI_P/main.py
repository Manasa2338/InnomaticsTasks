from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()

# ------------------ DATA ------------------

menu = [
    {"id": 1, "name": "Margherita Pizza", "price": 250, "category": "Pizza", "is_available": True},
    {"id": 2, "name": "Veg Burger", "price": 120, "category": "Burger", "is_available": True},
    {"id": 3, "name": "Coke", "price": 50, "category": "Drink", "is_available": True},
    {"id": 4, "name": "Brownie", "price": 90, "category": "Dessert", "is_available": False},
    {"id": 5, "name": "Pepperoni Pizza", "price": 350, "category": "Pizza", "is_available": True},
    {"id": 6, "name": "French Fries", "price": 100, "category": "Snack", "is_available": True}
]

orders = []
order_counter = 1
cart = []

# ------------------ HOME ------------------

@app.get("/")
def home():
    return {"message": "Welcome to QuickBite Food Delivery"}

# ------------------ MENU ------------------

@app.get("/menu")
def get_menu():
    return {"total": len(menu), "items": menu}

@app.get("/menu/summary")
def menu_summary():
    available = sum(1 for item in menu if item["is_available"])
    categories = list(set(item["category"] for item in menu))

    return {
        "total": len(menu),
        "available": available,
        "unavailable": len(menu) - available,
        "categories": categories
    }

@app.get("/menu/{item_id}")
def get_item(item_id: int):
    for item in menu:
        if item["id"] == item_id:
            return item
    return {"error": "Item not found"}

# ------------------ ORDERS ------------------

@app.get("/orders")
def get_orders():
    return {"total_orders": len(orders), "orders": orders}

# ------------------ MODELS ------------------

class OrderRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    item_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0, le=20)
    delivery_address: str = Field(..., min_length=10)
    order_type: str = "delivery"

class NewMenuItem(BaseModel):
    name: str = Field(..., min_length=2)
    price: int = Field(..., gt=0)
    category: str = Field(..., min_length=2)
    is_available: bool = True

class CheckoutRequest(BaseModel):
    customer_name: str
    delivery_address: str

# ------------------ HELPERS ------------------

def find_menu_item(item_id):
    for item in menu:
        if item["id"] == item_id:
            return item
    return None

def calculate_bill(price, quantity, order_type):
    total = price * quantity
    if order_type == "delivery":
        total += 30
    return total

def filter_menu_logic(category, max_price, is_available):
    result = menu

    if category is not None:
        result = [i for i in result if i["category"].lower() == category.lower()]

    if max_price is not None:
        result = [i for i in result if i["price"] <= max_price]

    if is_available is not None:
        result = [i for i in result if i["is_available"] == is_available]

    return result

# ------------------ CREATE ORDER ------------------

@app.post("/orders")
def place_order(order: OrderRequest):
    global order_counter

    item = find_menu_item(order.item_id)
    if not item:
        return {"error": "Item not found"}

    if not item["is_available"]:
        return {"error": "Item not available"}

    total = calculate_bill(item["price"], order.quantity, order.order_type)

    new_order = {
        "order_id": order_counter,
        "customer_name": order.customer_name,
        "item": item["name"],
        "quantity": order.quantity,
        "total_price": total
    }

    orders.append(new_order)
    order_counter += 1

    return new_order

# ------------------ FILTER ------------------

@app.get("/menu/filter")
def filter_menu(category: str = None, max_price: int = None, is_available: bool = None):
    filtered = filter_menu_logic(category, max_price, is_available)
    return {"count": len(filtered), "items": filtered}

# ------------------ CRUD ------------------

@app.post("/menu")
def add_item(item: NewMenuItem):
    for m in menu:
        if m["name"].lower() == item.name.lower():
            return {"error": "Item already exists"}

    new_item = item.dict()
    new_item["id"] = len(menu) + 1
    menu.append(new_item)

    return new_item

@app.put("/menu/{item_id}")
def update_item(item_id: int, price: int = None, is_available: bool = None):
    item = find_menu_item(item_id)
    if not item:
        return {"error": "Item not found"}

    if price is not None:
        item["price"] = price

    if is_available is not None:
        item["is_available"] = is_available

    return item

@app.delete("/menu/{item_id}")
def delete_item(item_id: int):
    item = find_menu_item(item_id)
    if not item:
        return {"error": "Item not found"}

    menu.remove(item)
    return {"message": f"{item['name']} deleted"}

# ------------------ CART ------------------

@app.post("/cart/add")
def add_to_cart(item_id: int, quantity: int = 1):
    item = find_menu_item(item_id)

    if not item or not item["is_available"]:
        return {"error": "Item not available"}

    for c in cart:
        if c["item_id"] == item_id:
            c["quantity"] += quantity
            return {"message": "Updated quantity", "cart": cart}

    cart.append({"item_id": item_id, "quantity": quantity})
    return {"message": "Added to cart", "cart": cart}

@app.get("/cart")
def view_cart():
    total = 0
    detailed = []

    for c in cart:
        item = find_menu_item(c["item_id"])
        cost = item["price"] * c["quantity"]
        total += cost

        detailed.append({
            "name": item["name"],
            "quantity": c["quantity"],
            "cost": cost
        })

    return {"cart": detailed, "grand_total": total}

@app.post("/cart/checkout")
def checkout(data: CheckoutRequest):
    global order_counter

    if not cart:
        return {"error": "Cart is empty"}

    new_orders = []
    total = 0

    for c in cart:
        item = find_menu_item(c["item_id"])
        cost = item["price"] * c["quantity"]

        new_order = {
            "order_id": order_counter,
            "customer_name": data.customer_name,
            "item": item["name"],
            "quantity": c["quantity"],
            "total_price": cost
        }

        new_orders.append(new_order)
        orders.append(new_order)

        order_counter += 1
        total += cost

    cart.clear()

    return {"orders": new_orders, "total": total}

# ------------------ ADVANCED ------------------

@app.get("/menu/search")
def search_menu(keyword: str):
    result = [i for i in menu if keyword.lower() in i["name"].lower()]

    if not result:
        return {"message": "No items found"}

    return {"total_found": len(result), "items": result}

@app.get("/menu/sort")
def sort_menu(sort_by: str = "price", order: str = "asc"):
    if sort_by not in ["price", "name", "category"]:
        return {"error": "Invalid sort_by"}

    reverse = True if order == "desc" else False
    return sorted(menu, key=lambda x: x[sort_by], reverse=reverse)

@app.get("/menu/page")
def paginate(page: int = 1, limit: int = 3):
    start = (page - 1) * limit
    total_pages = (len(menu) + limit - 1) // limit

    return {
        "page": page,
        "limit": limit,
        "total": len(menu),
        "total_pages": total_pages,
        "items": menu[start:start + limit]
    }

@app.get("/orders/search")
def search_orders(customer_name: str):
    return [o for o in orders if customer_name.lower() in o["customer_name"].lower()]

@app.get("/orders/sort")
def sort_orders(order: str = "asc"):
    reverse = True if order == "desc" else False
    return sorted(orders, key=lambda x: x["total_price"], reverse=reverse)

@app.get("/menu/browse")
def browse(keyword: str = None, sort_by: str = "price", order: str = "asc", page: int = 1, limit: int = 4):
    result = menu

    if keyword:
        result = [i for i in result if keyword.lower() in i["name"].lower()]

    reverse = True if order == "desc" else False
    result = sorted(result, key=lambda x: x[sort_by], reverse=reverse)

    start = (page - 1) * limit

    return {
        "total": len(result),
        "page": page,
        "items": result[start:start + limit]
    }