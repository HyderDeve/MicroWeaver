from fastapi import APIRouter
from app.models.user import User

router = APIRouter()

@router.get("/users")
async def get_users():
    return [{"id": 1, "name": "John Doe"}]

@router.post("/users")
async def create_user(user: User):
    return {"message": "User created", "user": user}