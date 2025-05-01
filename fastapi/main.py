from fastapi import FastAPI
from User import User_Router
from Role import Role_Router
from Supplier import Supplier_Router
from Pay import Pay_Router
from Order import Order_Router
from Report import Report_Router
from Inventory import Inventory_Router
from Egg import Egg_Router
from Bill import Bill_Router

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

app.include_router(User_Router.router, prefix="/User/User_Router")
app.include_router(Role_Router.router, prefix="/Role/Role_Router")
app.include_router(Supplier_Router.router, prefix="/User/Supplier_Router")
app.include_router(Pay_Router.router, prefix="/User/Pay_Router")
app.include_router(Order_Router.router, prefix="/User/Order_Router")
app.include_router(Report_Router.router, prefix="/User/Report_Router")
app.include_router(Inventory_Router.router, prefix="/User/Inventory_Router")
app.include_router(Egg_Router.router, prefix="/User/Egg_Router")
app.include_router(Bill_Router.router, prefix="/User/Bill_Router")