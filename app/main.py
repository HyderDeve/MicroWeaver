from fastapi import FastAPI
from app.routes import users

app = FastAPI()
app.include_router(users.router, prefix="/api/v1", tags=['users'])

@app.get("/")
async def root():
    return {"message": "MicroWeaver Microservice Generator API"}