from models.user import User as UserModel
from schemas.user import User
from fastapi.responses import JSONResponse
from utils.jwt_manager import create_token
from config.database import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException 

auth_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


#LOGIN
@auth_router.post("/login", tags=["Auth"], response_model= dict, status_code=200)
def login(user:User):
    db = Session()
    result = db.query(UserModel).filter(UserModel.username == user.username).first()
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    if result.password != user.password:
        raise HTTPException(status_code=404, detail="Password incorrect")
    token = create_token(data=user.model_dump())
    return JSONResponse(content={"message":"Login successfully","token":token},status_code=200)
