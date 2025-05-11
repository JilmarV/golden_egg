from fastapi import FastAPI
from app.User import user_router
from app.Role import Role_Router, Role_Model
from fastapi.app.Supplier import supplier_router
from app.Pay import Pay_Router, Pay_Model
from app.Order import Order_Router, Order_Model
from app.Report import Report_Router, Report_Model
from app.Egg import Egg_Router, Egg_Model
from app.Bill import Bill_Router, Bill_Model
from app.OrderEgg import OrderEgg_Model
from app.TypeEgg import typeegg_model
from app.UserRole import userrole_model
from app.WebVisit import webvisit_router, webvisit_model

from app.db.database import engine

import os

from fastapi.app.Supplier import supplier_model
from fastapi.app.User import user_model

user_model.Base.metadata.create_all(bind=engine)
Role_Model.Base.metadata.create_all(bind=engine)
supplier_model.Base.metadata.create_all(bind=engine)
Pay_Model.Base.metadata.create_all(bind=engine)
Order_Model.Base.metadata.create_all(bind=engine)
Report_Model.Base.metadata.create_all(bind=engine)
Egg_Model.Base.metadata.create_all(bind=engine)
Bill_Model.Base.metadata.create_all(bind=engine)
OrderEgg_Model.Base.metadata.create_all(bind=engine)
typeegg_model.Base.metadata.create_all(bind=engine)
userrole_model.Base.metadata.create_all(bind=engine)
webvisit_model.Base.metadata.create_all(bind=engine)

# FastAPI app
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

app.include_router(user_router.router, prefix="/User/User_Router")
app.include_router(Role_Router.router, prefix="/Role/Role_Router")
app.include_router(supplier_router.router, prefix="/User/Supplier_Router")
app.include_router(Pay_Router.router, prefix="/User/Pay_Router")
app.include_router(Order_Router.router, prefix="/User/Order_Router")
app.include_router(Report_Router.router, prefix="/User/Report_Router")
app.include_router(Egg_Router.router, prefix="/User/Egg_Router")
app.include_router(Bill_Router.router, prefix="/User/Bill_Router")
app.include_router(webvisit_router.router, prefix="/WebVisit/webvisit_router")