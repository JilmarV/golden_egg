"""Main entry point for FastAPI application, including all routers and database initialization."""

# pylint: disable=import-error, no-name-in-module, too-few-public-methods

# App module imports
from app.db.database import engine
from app.User import user_router, user_model
from app.Role import role_router, role_model
from app.Supplier import supplier_router, supplier_model
from fastapi.app.Pay import pay_router
from app.Order import Order_Router, Order_Model
from app.Report import report_router, report_model
from app.Egg import Egg_Router, Egg_Model
from app.Bill import Bill_Router, Bill_Model
from app.OrderEgg import OrderEgg_Model
from app.TypeEgg import typeegg_model
from app.UserRole import userrole_model
from app.WebVisit import webvisit_router, webvisit_model
from fastapi import FastAPI
from fastapi.app.Pay import pay_model

# Create all tables
user_model.Base.metadata.create_all(bind=engine)
role_model.Base.metadata.create_all(bind=engine)
supplier_model.Base.metadata.create_all(bind=engine)
pay_model.Base.metadata.create_all(bind=engine)
Order_Model.Base.metadata.create_all(bind=engine)
report_model.Base.metadata.create_all(bind=engine)
Egg_Model.Base.metadata.create_all(bind=engine)
Bill_Model.Base.metadata.create_all(bind=engine)
OrderEgg_Model.Base.metadata.create_all(bind=engine)
typeegg_model.Base.metadata.create_all(bind=engine)
userrole_model.Base.metadata.create_all(bind=engine)
webvisit_model.Base.metadata.create_all(bind=engine)

# FastAPI app initialization
app = FastAPI(
    title="FastAPI",
    root_path="/api",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,
        "persistAuthorization": True,
    },
)

# Routers
app.include_router(user_router.router, prefix="/User/User_Router")
app.include_router(role_router.router, prefix="/Role/Role_Router")
app.include_router(supplier_router.router, prefix="/User/Supplier_Router")
app.include_router(pay_router.router, prefix="/User/Pay_Router")
app.include_router(Order_Router.router, prefix="/User/Order_Router")
app.include_router(report_router.router, prefix="/User/Report_Router")
app.include_router(Egg_Router.router, prefix="/User/Egg_Router")
app.include_router(Bill_Router.router, prefix="/User/Bill_Router")
app.include_router(webvisit_router.router, prefix="/WebVisit/webvisit_router")
