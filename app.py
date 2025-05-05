from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


app = FastAPI()
client = MongoClient("mongodb://mongo:27017/")
db = client["smartstock_analytics"]

class SalesData(BaseModel):
    date: datetime
    quantity: int

class ProductAnalytics(BaseModel):
    product_id: int
    current_stock: int
    sales_history: list[SalesData] = []
    alert_status: bool = False




# Endpoints CRUD básicos
@app.post("/products/", status_code=201)
async def create_product(product: ProductAnalytics):
    db.products.insert_one(product.dict())
    return {"message": "Product analytics created"}

@app.get("/products/{product_id}")
async def get_product(product_id: int):
    product = db.products.find_one({"product_id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product["_id"] = str(product["_id"])  # Convertir ObjectId a string
    return product

@app.put("/products/{product_id}/stock")
async def update_stock(product_id: int, new_stock: int):
    result = db.products.update_one(
        {"product_id": product_id},
        {"$set": {"current_stock": new_stock}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Product not updated")
    return {"message": "Stock updated"}

# Endpoint de salud para verificar que el servicio está activo
@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": datetime.now()}