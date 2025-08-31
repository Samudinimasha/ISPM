from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.user import User, UserRole
from backend.utils.security import verify_password, get_password_hash, create_access_token
from pydantic import BaseModel
import jwt

router = APIRouter(prefix="/auth", tags=["auth"])

# JWT configuration
SECRET_KEY = "your-secret-key"  # Replace with secure key
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Pydantic models
class UserCreate(BaseModel):
    email: str
    password: str
    role: UserRole = UserRole.employee

class UserUpdate(BaseModel):
    email: str | None = None
    password: str | None = None

class UserLogin(BaseModel):
    email: str
    password: str
    role: str

class UserResponse(BaseModel):
    email: str
    role: str
    class Config:
        orm_mode = True

# Dependency to get current user and enforce admin role
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        role = payload.get("role")
        if not user_id or not role:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return {"id": user.id, "email": user.email, "role": user.role.value}
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

@router.post("/register")
def register(user: UserCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admins only")
    
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User registered successfully", "id": new_user.id}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    if user.role != db_user.role.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Selected role does not match your account")

    access_token = create_access_token(data={"sub": str(db_user.id), "role": db_user.role.value})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"email": db_user.email, "role": db_user.role.value}
    }

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admins only")
    
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_update.email:
        db_user.email = user_update.email
    if user_update.password:
        db_user.hashed_password = get_password_hash(user_update.password)
    
    db.commit()
    db.refresh(db_user)
    return {"email": db_user.email, "role": db_user.role.value}