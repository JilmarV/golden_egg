from fastapi import FastAPI
from User import User_router
from Role import Role_router
from UserRole import UserRole_router
from Supplier import Supplier_router
from fastapi.Pay import Pay_router
from fastapi.Order import Order_router
from fastapi.OrderEgg import OrderEgg_router
from fastapi.Report import Report_router
from Invetory import Inventory_Router
from Egg import Egg_Router

import os

# FastAPI app
app = FastAPI(
    title="FastAPI Example",
    root_path="/api",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,
        "persistAuthorization": True,
    },
)

app.include_router(User_router, prefix="/User/User_router")
app.include_router(Role_router, prefix="/Role/Role_router")
app.include_router(UserRole_router, prefix="/User/UserRole_router")
app.include_router(Supplier_router, prefix="/User/Supplier_router")
app.include_router(Pay_router, prefix="/User/Pay_router")
app.include_router(Order_router, prefix="/User/Order_router")
app.include_router(OrderEgg_router, prefix="/User/OrderEgg_router")
app.include_router(Report_router, prefix="/User/Report_router")