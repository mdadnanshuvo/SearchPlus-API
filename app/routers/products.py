from fastapi import APIRouter
from typing import List
from app.schemas.product import Product
from app.services.product_service import (
    index_product, batch_index, search_products, autocomplete, category_analytics
)


router = APIRouter(prefix="/products")

@router.post("/add")
def add_product(product: Product):
    index_product(product)
    return {"status": "ok", "product": product}

@router.post("/batch")
def add_products(products: List[Product]):
    batch_index(products)
    return {"status": "ok", "product":products}

@router.get("/search")
def search(q: str, page: int = 1, size: int = 10, sort_by: str = "price"):
    return search_products(q, page, size, sort_by)

@router.get("/autocomplete")
def auto(q: str):
    return autocomplete(q)

@router.get("/analytics")
def analytics():
    return category_analytics()




