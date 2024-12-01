from fastapi import FastAPI
from app.routes import posts, users
from app.database import Base, engine

# Initialize the FastAPI app
app = FastAPI()

# Create all tables in the database (only for development)
Base.metadata.create_all(bind=engine)

# Include Routers for Users and Posts
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])

# Root Endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Blog API!"}
