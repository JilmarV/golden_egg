"""Main entry point for FastAPI application, including all routers and database initialization."""

# App module imports
from app.db.database import engine
from app.User import user_router, user_model
from app.Role import role_router, role_model
from app.Supplier import supplier_router, supplier_model
from app.Pay import pay_router, pay_model
from app.Order import order_router, order_model
from app.Report import report_router, report_model
from app.Egg import egg_router, egg_model
from app.Bill import bill_router, bill_model
from app.OrderEgg import order_egg_model, order_egg_router
from app.TypeEgg import typeegg_model, typeegg_router
from app.UserRole import userrole_model
from app.WebVisit import webvisit_router, webvisit_model
from app.Auth import auth_router
from fastapi import FastAPI

# Create all tables
user_model.Base.metadata.create_all(bind=engine)
role_model.Base.metadata.create_all(bind=engine)
supplier_model.Base.metadata.create_all(bind=engine)
pay_model.Base.metadata.create_all(bind=engine)
order_model.Base.metadata.create_all(bind=engine)
report_model.Base.metadata.create_all(bind=engine)
egg_model.Base.metadata.create_all(bind=engine)
bill_model.Base.metadata.create_all(bind=engine)
order_egg_model.Base.metadata.create_all(bind=engine)
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
        "defaultmodelsExpandDepth": -1,
        "persistAuthorization": True,
    },
)

# PYTHONPATH=/app pytest

# routers
app.include_router(user_router.router, prefix="/user")
app.include_router(role_router.router, prefix="/role")
app.include_router(supplier_router.router, prefix="/supplier")
app.include_router(pay_router.router, prefix="/pay")
app.include_router(order_router.router, prefix="/order")
app.include_router(report_router.router, prefix="/report")
app.include_router(egg_router.router, prefix="/egg")
app.include_router(typeegg_router.router, prefix="/typeeggs")
app.include_router(order_egg_router.router, prefix="/orderegg")
app.include_router(bill_router.router, prefix="/bill")
app.include_router(webvisit_router.router, prefix="/visit")
app.include_router(auth_router.router)
