from fastapi import FastAPI, HTTPException
from db import client, users_collection, policies_collection, training_collection

app = FastAPI(title="ISPM Backend API", version="1.0")

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# MongoDB health check
@app.get("/ping-db")
def ping_db():
    try:
        client.admin.command("ping")
        return {"status": "MongoDB connected ✅"}
    except Exception as e:
        return {"status": "MongoDB connection failed ❌", "error": str(e)}

# Users endpoint
@app.get("/users")
def get_users():
    try:
        users = list(users_collection.find({}, {"_id": 0}))  # Exclude _id
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Policies endpoint
@app.get("/policies")
def get_policies():
    try:
        policies = list(policies_collection.find({}, {"_id": 0}))
        return {"policies": policies}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Training endpoint
@app.get("/training")
def get_training():
    try:
        trainings = list(training_collection.find({}, {"_id": 0}))
        return {"training": trainings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
