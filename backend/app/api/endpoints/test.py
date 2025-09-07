from fastapi import Depends, APIRouter, HTTPException

from sqlmodel import Session, select

from app.models.database import get_session
from app.models.test import User, UserCreate, UserRead, UserUpdate

router = APIRouter()

@router.post("/users/", response_model=UserRead)
def create_user(*, session: Session = Depends(get_session), user: UserCreate):
    target_user = User(
        user_name=user.user_name,
        email=user.email
    )
    session.add(target_user)
    session.commit()
    session.refresh(target_user)
    return target_user

@router.get("/users/{user_name}", response_model=UserRead)
def read_user(*, session: Session = Depends(get_session), user_name: str):
    target_user = session.exec(
        select(User).where(User.user_name == user_name)
    ).one_or_none()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    return target_user

@router.patch("/users/{user_name}", response_model=UserRead)
def update_user(*, session: Session = Depends(get_session), user_name: str, user: UserUpdate):
    target_user = session.exec(
        select(User).where(User.user_name == user_name)
    ).one_or_none()

    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user.model_dump(exclude_unset=True)

    if 'user_id' in update_data:
        del update_data['user_id']

    for field_name, new_value in update_data.items():
        setattr(target_user, field_name, new_value)
    session.add(target_user)
    session.commit()
    session.refresh(target_user)
    return target_user

@router.delete("/users/{user_name}", status_code=204)
def delete_user(*, session: Session = Depends(get_session), user_name: str):
    target_user = session.exec(
        select(User).where(User.user_name == user_name)
    ).one_or_none()

    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(target_user)
    session.commit()
    return None
