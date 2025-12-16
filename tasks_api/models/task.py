from pydantic import BaseModel

class Task(BaseModel):
    name: str
    text: str
    state: str = "Awaiting completion" 