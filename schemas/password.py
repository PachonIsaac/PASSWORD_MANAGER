from pydantic import BaseModel
from datetime import date

class Password(BaseModel):
    passwordID : int
    userID: int
    creation_password: date
    password: str
    