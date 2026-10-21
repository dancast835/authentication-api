from sqlmodel import Field, SQLModel, create_engine, select, Session
from app.config import DATABASE_URL


#------------------------------------------- Database Set up --------------------------------------------------#

class UserData(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(nullable=False, unique=True)
    password_hash: str = Field(nullable=False)



engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
)

#------------------------------------------- Database functions  --------------------------------------------------#
#this should be program to only create the table if it doesn't exist
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

#session
##avoids connection leaks
##sessions are open and closed properly
def get_session():
    with Session(engine) as session:
        yield session
        


def create_user(user: UserData, session: Session):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


#maybe by id check if needed
def get_user_by_email(email: str, session:Session):
    user_email = select(UserData).where(UserData.email == email)
    user = session.exec(user_email).first()

    if not user:
        return False
    else: 
        return user
    
def change_password(email:str, hash: str, session:Session):
    #TODO: update to use the get_user_by_email function
    user_email = select(UserData).where(UserData.email == email)
    user = session.exec(user_email).first() 
    if user:
        user.password_hash = hash
        session.commit()
        return True
    else: 
        return False

def delete_user(email: str, session:Session):
    user_email = select(UserData).where(UserData.email == email)
    user = session.exec(user_email).first() 
    if user:
        session.delete(user)
        session.commit()
        return True
    else:
        return False