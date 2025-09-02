# app/routes/admin.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.models import user as user_models, course as course_models, quiz as quiz_models
from app.schemas import user as user_schemas, course as course_schemas
from app.core.security import get_current_user, admin_required
from app.database import get_db

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(admin_required)]  #only admins can access
)

# ----------------------------
# USER MANAGEMENT
# ----------------------------

@router.get("/users", response_model=List[user_schemas.UserOut])
def list_users(db: Session = Depends(get_db)):
    """List all employees and admins"""
    return db.query(user_models.User).all()

@router.post("/users/promote/{user_id}")
def promote_to_admin(user_id: int, db: Session = Depends(get_db)):
    """Promote a user to admin"""
    user = db.query(user_models.User).filter(user_models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.role = "admin"
    db.commit()
    return {"msg": f"User {user.email} promoted to admin"}

@router.delete("/users/{user_id}")
def deactivate_user(user_id: int, db: Session = Depends(get_db)):
    """Deactivate a user (soft delete)"""
    user = db.query(user_models.User).filter(user_models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = False
    db.commit()
    return {"msg": f"User {user.email} deactivated"}

# ----------------------------
# COURSE MANAGEMENT
# ----------------------------

@router.post("/courses", response_model=course_schemas.CourseOut)
def create_course(course: course_schemas.CourseCreate, db: Session = Depends(get_db)):
    """Create a new course"""
    new_course = course_models.Course(**course.dict())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

@router.put("/courses/{course_id}", response_model=course_schemas.CourseOut)
def update_course(course_id: int, course: course_schemas.CourseUpdate, db: Session = Depends(get_db)):
    """Update a course"""
    db_course = db.query(course_models.Course).filter(course_models.Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    for key, value in course.dict(exclude_unset=True).items():
        setattr(db_course, key, value)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.delete("/courses/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    """Delete a course"""
    db_course = db.query(course_models.Course).filter(course_models.Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(db_course)
    db.commit()
    return {"msg": "Course deleted"}

# ----------------------------
# COMPLIANCE TRACKING
# ----------------------------

@router.get("/compliance")
def compliance_report(db: Session = Depends(get_db)):
    """Generate compliance stats (who completed / not)"""
    report = []
    courses = db.query(course_models.Course).all()

    for course in courses:
        enrolled_users = course.enrollments  # assuming relationship is set
        completed = sum(1 for e in enrolled_users if e.is_completed)
        pending = len(enrolled_users) - completed
        report.append({
            "course": course.title,
            "total_enrolled": len(enrolled_users),
            "completed": completed,
            "pending": pending
        })

    return {"compliance_report": report}