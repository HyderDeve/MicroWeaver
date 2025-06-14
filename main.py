from fastapi import FastAPI
from app.routes.account import router as account_router  # Updated import
from app.routes.generator import router as generator_router  # Updated import
from app.routes.users import router as user_router  # Change user to users and user_route to user_router
from app.core.config import settings
from app.core.database import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


# Include API router
# Include API routers
app.include_router(account_router, prefix=settings.API_V1_STR)
app.include_router(generator_router, prefix=settings.API_V1_STR)
app.include_router(user_router, prefix=settings.API_V1_STR)  # Now this matches
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)