from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from config.database import Session
from models.user import User as UserModel
from models.password import Password as PasswordModel
from fastapi.encoders import jsonable_encoder
from schemas.password import Password
from typing import List
from utils.jwt_manager import validate_token
import random
from middlewares.jwt_bearer import JWTBearer

password_router = APIRouter()

#PEDIR UN HEADER CON EL TOKEN


#GET ALL PASSWORDS
@password_router.get("/password", tags=["Password"], response_model=List[Password],status_code=200, dependencies=[Depends(JWTBearer())])
def get_passwords() -> List[Password]:
    db = Session()
    result = db.query(PasswordModel).all()
    return JSONResponse (content=jsonable_encoder(result), status_code=200)
    

#CREATE PASSWORD
@password_router.post("/password", tags=["Password"], response_model= dict, status_code=201)
def create_password(password: Password ):
    db = Session()
    new_password = PasswordModel(**password.model_dump())
    new_password.password = generate_password(password.length,password.capital_letters,password.numbers,password.special_characters)
    db.add(new_password)
    db.commit()
    return JSONResponse(content={"message":"Password create successfully"},status_code=201)
   

#UPDATE PASSWORD BY ID
@password_router.put("/password/{password_id}", tags=["Password"], response_model= dict, status_code=201)
def update_password(password:Password):
    db = Session()
    result = db.query(PasswordModel).filter(PasswordModel.id == password.id).first()
    if not result:
        return HTTPException(status_code=404, detail="Password not found")
    result.password = generate_password(password.length,password.capital_letters,password.numbers,password.special_characters)
    db.commit()
    return JSONResponse(content={"message": "Password updated successfully"}, status_code=200)

#DELETE PASSWORD BY ID
@password_router.delete("/password/{password_id}", tags=["Password"], response_model= dict, status_code=201)
def delete_password(password_id:int):
    db = Session()
    result = db.query(PasswordModel).filter(PasswordModel.id == password_id).first()
    if not result:
        return HTTPException(status_code=404, detail="Password not found")
    db.delete(result)
    db.commit()
    return JSONResponse(content={"message": "Password deleted successfully"}, status_code=200)


#Password generation function
def generate_password(length, capital_letters, numbers, special_characters):
        minusculas = length - (capital_letters+numbers+special_characters)
        caracteres = []
        if capital_letters:
            caracteres += list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        if minusculas:
            caracteres += list("abcdefghijklmnopqrstuvwxyz")
        if numbers:
            caracteres += list("0123456789")
        if special_characters:
            caracteres += list("!@#$%^&*-_=+[]();:,.<>/?'")

        password = ""
        for _ in range(length):
            password += caracteres[random.randint(0, len(caracteres) - 1)]

        return password





