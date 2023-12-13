from fastapi import APIRouter, HTTPException, Path, Query, Depends
from fastapi.responses import JSONResponse, HTMLResponse
from config.database import Session
from models.user import User as UserModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from schemas.user import User
from typing import List

user_router = APIRouter()

#CREATE USER
@user_router.post("/user", tags=["User"], response_model= dict, status_code=201)
def create_user(user: User):
    db = Session()
    new_user = UserModel(**user.model_dump())
    db.add(new_user)
    db.commit()
    return JSONResponse(content={"message":"User create successfully"},status_code=201)

#GET ALL THE USERS
@user_router.get("/user", tags=["User"], response_model= dict, status_code=201)
def get_all_users():
    db = Session()
    result = db.query(UserModel).all()
    return JSONResponse (content=jsonable_encoder(result), status_code=200)


