from pydantic import BaseModel

class User(BaseModel):
    userID: int
    username: str
    password: str
    disabled: bool | None = None

            