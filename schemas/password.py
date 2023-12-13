from pydantic import BaseModel
from datetime import date

class Password(BaseModel):
    id : int
    length: int 
    special_characters: int
    numbers: int
    capital_letters: int
    creation_password: date
    password: str
    id_user: int