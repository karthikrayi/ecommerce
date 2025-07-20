from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from bson import ObjectId
from app.database import db
from app.schemas.models import ProductCreate, ProductOut, OrderCreate, OrderOut
from fastapi.responses import JSONResponse

router = APIRouter()


def to_str_id(doc):
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc


@router.post("/products", status_code=201)
async def create_product(product: ProductCreate):
    result = await db.products.insert_one(product.dict())
    return {"id": str(result.inserted_id)}


@router.get("/products")
async def list_products(
    name: Optional[str] = None,
    size: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
):
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if size:
        query["sizes"] = {"$elemMatch": {"size": size}}

    total_products = await db.products.count_documents(query)
    cursor = db.products.find(query).skip(offset).limit(limit)
    products = []
    async for doc in cursor:
        products.append({
            "id": str(doc["_id"]),
            "name": doc["name"],
            "price": doc["price"]
        })

    page = {
        "next": str(offset + limit) if (offset + limit) < total_products else None,
        "limit": len(products),
        "previous": max(offset - limit, 0)
    }

    return {
        "data": products,
        "page": page
    }


@router.post("/orders", status_code=201)
async def create_order(order: OrderCreate):
    order_dict = order.dict()
    order_dict["items"] = [{"productId": ObjectId(item["productId"]), "qty": item["qty"]} for item in order_dict["items"]]
    result = await db.orders.insert_one(order_dict)
    return {"id": str(result.inserted_id)}


@router.get("/orders/{user_id}")
async def get_orders(user_id: str, limit: int = 10, offset: int = 0):
    query = {"userId": user_id}
    total_orders = await db.orders.count_documents(query)

    cursor = db.orders.find(query).skip(offset).limit(limit)
    results = []

    async for order in cursor:
        items = []
        total = 0.0

        for item in order["items"]:
            product = await db.products.find_one({"_id": item["productId"]})
            if product:
                product_detail = {
                    "id": str(product["_id"]),
                    "name": product["name"],
                    "qty": item["qty"]
                }
                total += product["price"] * item["qty"]
                items.append(product_detail)
            else:
                print(f"Product not found: {item['productId']}")
        results.append({
            "id": str(order["_id"]),
            "items": items,
            "total": total
        })

    page = {
        "next": str(offset + limit) if (offset + limit) < total_orders else None,
        "limit": len(results),
        "previous": max(offset - limit, 0)
    }

    return {
        "data": results,
        "page": page
    }
