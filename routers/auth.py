from models.user import User as UserModel
from schemas.user import User
from fastapi.responses import JSONResponse
from utils.jwt_manager import create_token , validate_token
from config.database import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException 
from typing import Annotated
from jwt import PyJWTError
auth_router = APIRouter()

# Definir el esquema OAuth2 para manejar las credenciales del usuario
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

 # Función para obtener un usuario por su nombre de usuario desde la base de datos
def get_user(username: str):
    db = Session()
    user = db.query(UserModel).filter(UserModel.username == username).first()
    return user

# Función para decodificar un token JWT y obtener información del usuario
def decode_token(token):
    try:
        payload = validate_token(token)
        username: str = payload.get("sub")
        if username is None:
            return None
        user = get_user(username)
        return user
    except PyJWTError:
        return None

# Función para obtener el usuario actual basado en el token proporcionado
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = decode_token(token)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user

# Función para obtener el usuario activo actual basado en el token proporcionado
async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Ruta para autenticar y generar un token de acceso
@auth_router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = get_user(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    password = form_data.password
    if not password == user.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_token(data={"sub": user.username})
    return JSONResponse(content={"access_token": token, "token_type": "bearer"})

# Ruta para obtener la información del usuario actual
@auth_router.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user