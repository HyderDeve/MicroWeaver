from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str = "John Doe"
    email: str | None = None