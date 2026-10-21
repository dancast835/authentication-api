from fastapi import APIRouter, Depends
from pydantic import EmailStr
from typing import Annotated
from sqlmodel import Session

from app.database.db import *
from app.auth.hash_password import *
from services.JWT import *

#------------------------------------------- FastAPI Setup --------------------------------------------------#
# To run the program 
#fastapi dev app/routes/routes.py

#Request body to send data
class User(BaseModel):
    email: EmailStr
    password: str

router = APIRouter()

#------------------------------------------- Endpoints --------------------------------------------------#
SessionDep = Annotated[Session, Depends(get_session)]

@router.post("/signup")
def signup(user: User, session: SessionDep):
    hash = secure_password(user.password)
    db_user = UserData(email=user.email, password_hash=hash)
    create_user(db_user, session)

    return {"message": "User registered successfully"}


@router.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    email = form_data.username
    password = form_data.password
    db_user = get_user_by_email(email, session)


    if db_user:
        verified = verify_password(password, db_user.password_hash)

        if verified:
            access_token = create_access_token(
                data={"sub": db_user.email}
            )
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "message": "Login Successful"
            }


    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.put("/update")
def update(user: User, session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]):
    username = verify_token(token)
    
    if username == user.email:
        new_hash = secure_password(user.password)
        complete = change_password(user.email, new_hash, session)

        if complete:
            return {"message": "Password change successfully!"}
    else:
        raise credentials_exception
    

@router.delete("/delete")
def delete(user: User, session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]):
    username = verify_token(token)

    if username == user.email:
        complete = delete_user(user.email, session)

        if complete:
            return {"message": "User deleted Successfully"}
              
    else:
        raise credentials_exception
