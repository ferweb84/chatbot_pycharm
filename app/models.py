from pydantic import BaseModel
from typing import List


class User(BaseModel):
    username: str
    name: str
    age: int


class Message(BaseModel):
    text: str
