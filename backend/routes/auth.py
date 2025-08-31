from fastapi import APIRouter, HTTPException
from app.utils.database import users_collection

router = APIRouter()

@router.post("/register")
def register_user(user: dict):
    # Check if email already exists
    if users_collection.find_one({"email": user["email"]}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    result = users_collection.insert_one(user)
    user["_id"] = str(result.inserted_id)
    return {"msg": "User registered successfully", "user": user}

@router.post("/login")
def login_user(data: dict):
    user = users_collection.find_one({"email": data["email"], "password": data["password"]})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user["_id"] = str(user["_id"])
    return {"msg": "Login successful", "user": user}
