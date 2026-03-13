from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Annotated
import jwt
from jwt.exceptions import InvalidTokenError

from datetime import datetime, timedelta, timezone

from sqlmodel import Session, select
from app.database.db import UserData, get_session, create_user, change_password, delete_user, get_user_by_email
from app.auth.hash_password import secure_password, verify_password
from app.config import SECRET_KEY, ALGORITHM

#------------------------------------------- FastAPI Setup --------------------------------------------------#
# To run the program 
#fastapi dev app/routes/routes.py

#Request body to send data
class User(BaseModel):
    email: str
    password: str

router = APIRouter()

#------------------------------------------- JWT Setup --------------------------------------------------#

class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise credentials_exception
        
        return username

    except InvalidTokenError:
        raise credentials_exception


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"})

#------------------------------------------- DataBase Endpoints --------------------------------------------------#
SessionDep = Annotated[Session, Depends(get_session)]

@router.post("/signup")
def signup(user: User, session: SessionDep):
    hash = secure_password(user.password)
    db__user = UserData(email=user.email, password_hash=hash)
    create_user(db__user, session)
    
    return {"message": "User registered successfully"}

@router.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    email = form_data.username
    password = form_data.password
    db_user = get_user_by_email(email, session)
    
    if not db_user:
        return {"message": "User not Found"}
    else:
        verified = verify_password(password, db_user.password_hash)
        if verified:
            access_token = create_access_token(
                data={"sub": db_user.email}
            )
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "message": "Login Succesful"
            }

@router.put("/update")
def update(user: User, session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]):

    username = verify_token(token)
    
    if username == user.email:
        new_hash = secure_password(user.password)
        complete = change_password(user.email, new_hash, session)

        if complete:
            return {"message": "Password change successfully!"}
    else:
        return {"message": "Not allowed"}
    

@router.delete("/delete")
def delete(user: User, session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    if username == user.email:
        complete = delete_user(user.email, session)

        if complete:
            return {"message": "User deleted Successfully"}
              
    else:
        return{"message": "Not allowed"}
