
from fastapi import FastAPI
from api.v1.item_routes import router as item_router

app = FastAPI()

app.include_router(item_router, prefix="/api/v1/item")
