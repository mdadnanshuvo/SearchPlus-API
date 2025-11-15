from fastapi import FastAPI
from app.index.product_index import create_product_index
from app.routers.products import router as product_router
from app.es_client import es
app = FastAPI(title="SearchPlus API")

@app.on_event("startup")
def startup():
    create_product_index()

    
app.include_router(product_router)
