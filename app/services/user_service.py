from sqlalchemy.orm import Session
from app.repositories.user_repository import (
    create_user as repo_create_user,
    get_user as repo_get_user,
    update_user as repo_update_user,
    delete_user as repo_delete_user,
    get_users as repo_get_users
)
from app.schemas.user import UserCreate, UserUpdate

def create_user(db: Session, user: UserCreate):
    return repo_create_user(db, user)

def get_user(db: Session, user_id: int):
    return repo_get_user(db, user_id)

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return repo_get_users(db, skip=skip, limit=limit)

def update_user(db: Session, user_id: int, user: UserUpdate):
    return repo_update_user(db, user_id, user)

def delete_user(db: Session, user_id: int):
    return repo_delete_user(db, user_id)
