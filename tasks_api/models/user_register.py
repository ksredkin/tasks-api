from pydantic import BaseModel

class UserRegister(BaseModel):
    login: str
    password: str