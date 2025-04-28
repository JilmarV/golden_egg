from fastapi import FastAPI
from fastapi.User import User_Router
from fastapi.Role import Role_Router
from fastapi.UserRole import UserRole_Router
from fastapi.Supplier import Supplier_Router
from fastapi.Pay import Pay_Router
from fastapi.Order import Order_Router
from fastapi.OrderEgg import OrderEgg_Router
from fastapi.Report import Report_Router
from fastapi.Inventory import Inventory_Router
from fastapi.Egg import Egg_Router
from fastapi.Bill import Bill_Router

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

app.include_router(User_Router, prefix="/User/User_Router")
app.include_router(Role_Router, prefix="/Role/Role_Router")
app.include_router(UserRole_Router, prefix="/User/UserRole_Router")
app.include_router(Supplier_Router, prefix="/User/Supplier_Router")
app.include_router(Pay_Router, prefix="/User/Pay_Router")
app.include_router(Order_Router, prefix="/User/Order_Router")
app.include_router(OrderEgg_Router, prefix="/User/OrderEgg_Router")
app.include_router(Report_Router, prefix="/User/Report_Router")
app.include_router(Inventory_Router, prefix="/User/Inventory_Router")
app.include_router(Egg_Router, prefix="/User/Egg_Router")
app.include_router(Bill_Router, prefix="/User/Bill_Router")