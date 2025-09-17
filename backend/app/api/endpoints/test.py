from datetime import timedelta
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlmodel import Session, select

from app.models.database import get_session
from app.models.test import User, UserCreate, UserRead, UserUpdate, Token
from app.utils.fastapi_user_auth import authenticate_user_db, create_access_token, get_current_active_user, get_password_hash

router = APIRouter()

#TODO:utilでも使っている変数だから共通化する
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# #DONE:これを使っている部分を本番のDBを検索する形に書き換える
# fake_users_db = {し
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
#         "disabled": False,
#     }
# }

@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
) -> Token:
    user = authenticate_user_db(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_name}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@router.post("/users/", response_model=UserRead)
def create_user(*, session: Session = Depends(get_session), user: UserCreate):
    target_user = User(
        user_name=user.user_name,
        email=user.email,
        hashed_password=get_password_hash(user.password)
    )
    session.add(target_user)
    session.commit()
    session.refresh(target_user)
    return target_user

# 怪
@router.get("/users/me", response_model=UserRead)
def read_user(
    *,
    current_user: User = Depends(get_current_active_user),  # 追加
    session: Session = Depends(get_session)
    ):

    authorized_me = current_user.user_name

    #TODO:仕様のチェック:current_user.user_nameがないということは、認証されていないとみなす
    if not authorized_me:
        raise HTTPException(status_code=403, detail="Not authorized")


    target_user = session.exec(
        select(User).where(User.user_name == authorized_me)
    ).one_or_none()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    return target_user

@router.get("/users/{user_name}", response_model=UserRead)
def read_user(
    *,
    session: Session = Depends(get_session), user_name: str
    ):

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
