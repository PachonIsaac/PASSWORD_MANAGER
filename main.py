from fastapi import FastAPI
from config.database import Base, engine
from middlewares.error_handler import ErrorHandler
from routers.password import password_router
from routers.user import user_router
from routers.auth import auth_router

app = FastAPI()
app.title = "PASSWORD MANAGER API"

app.add_middleware(ErrorHandler)
app.include_router(password_router)
app.include_router(user_router)
app.include_router(auth_router)
Base.metadata.create_all(bind=engine)