from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Backend is running!"}

from backend.routes import auth, policies, quizzes, training
from backend.database import Base, engine

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Routers
app.include_router(auth.router)
app.include_router(policies.router)
app.include_router(quizzes.router)
app.include_router(training.router)
app.include_router(admin.router)
