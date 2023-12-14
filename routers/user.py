from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from config.database import Session
from models.user import User as UserModel
from fastapi.encoders import jsonable_encoder
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from routers.auth import get_current_active_user

user_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


#CREATE USER
@user_router.post("/user", tags=["User"], response_model= dict, status_code=201)
def create_user(
    username: str = Query(..., description="Username of the user"),
    password: str = Query(..., description="Password of the user")
):
    db = Session()
    new_user = UserModel()
    new_user.username = username
    new_user.password = password
    db.add(new_user)
    db.commit()
    return JSONResponse(content={"message":"User create successfully"},status_code=201)


#GET ALL THE USERS
@user_router.get("/user", tags=["User"], response_model= dict, status_code=201)
def get_all_users():
    db = Session()
    result = db.query(UserModel).all()
    return JSONResponse (content=jsonable_encoder(result), status_code=200)


#DELETE USER
@user_router.put("/user/delete", tags=["User"], response_model= dict, status_code=201)
def delete_user(current_user: Annotated[UserModel, Depends(get_current_active_user)],
):
    db = Session()
    current_user.disabled = True
    db.commit()
    return JSONResponse(content={"message": "User deleted successfully"}, status_code=200)


#RECEOVER USER (PUT DISABLED = FALSE)
@user_router.put("/user/recover", tags=["User"], response_model= dict, status_code=201)
def recover_user(
    username: str = Query(..., description="Username of the user"),
    password: str = Query(..., description="Password of the user")
):
    db=Session()
    user_to_recover = db.query(UserModel).filter(UserModel.username == username).first()
    if user_to_recover is None:
        return HTTPException(status_code=404, detail="User not found")
    else:
        if user_to_recover.password == password:
            user_to_recover.disabled = False
            db.commit()
            return JSONResponse(content={"message": "User recovered successfully"}, status_code=200)
