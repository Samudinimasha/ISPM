from sqlalchemy import Column, Integer, String, Enum
from backend.database import Base
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    employer = "employer"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.employer, nullable=False)