from fastapi import APIRouter, status
from app.models.user import User

router = APIRouter()

@router.get("/users")
async def get_users():
    return [{"id": 1, "name": "John Doe"}]

@router.post("/users",status_code=status.HTTP_201_CREATED,)
async def create_user(user: User):
    return {"message": "User created", "user": user}