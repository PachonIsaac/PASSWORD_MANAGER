from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from utils.jwt_manager import validate_token


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if 'username' not in data or 'password' not in data:
            raise HTTPException(status_code=401, detail="Invalid user")