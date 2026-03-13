import pytest
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.pool import StaticPool
from app.database.db import UserData, create_user, get_user_by_email, change_password, delete_user


#------------------------------------------- Variables --------------------------------------------------#
EMAIL = "test@example.com"
PASSWORD_HASH = "hashedpassword123"
wrong_email = "wrong@example.com"

#------------------------------------------- Test database setup  -------------------------------------------------#
test_engine = create_engine(
    "sqlite://",                                    #creates an in-memory sqlite database
    connect_args={"check_same_thread": False},      #so SQlite behaves nicely in test context 
    poolclass=StaticPool,                           #to reuse the same in-memory connection during test
)

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        yield session

    SQLModel.metadata.drop_all(test_engine)


#------------------------------------------- Functions to Test  --------------------------------------------------#
def test_create_user(session):
    user = UserData(email=EMAIL, password_hash=PASSWORD_HASH)
    create_result = create_user(user, session)
    fetch_result = get_user_by_email(EMAIL, session)

    assert create_result is not None
    assert fetch_result is not False
    assert fetch_result.email == EMAIL
    assert user.password_hash == PASSWORD_HASH
    
# user is actually created in the DB
# returned user has the expected email
# stored object has a password hash value

def test_get_user_by_email(session):
    user = UserData(email=EMAIL, password_hash=PASSWORD_HASH)
    create_user(user, session)
    fetch_result = get_user_by_email(EMAIL, session)
    non_existing_user = get_user_by_email(wrong_email, session)

    assert fetch_result is not False
    assert fetch_result.email == EMAIL
    assert fetch_result.password_hash == PASSWORD_HASH
    assert non_existing_user is False
# existing email returns the correct user
# non-existing email returns None

def test_change_password(session):
    user = UserData(email=EMAIL, password_hash=PASSWORD_HASH)
    new_hash = "newhash123!"
    create_user(user, session)

    fetch_result = get_user_by_email(EMAIL, session)
    change_result = change_password(EMAIL, new_hash, session)
    non_existing_user = change_password(wrong_email, new_hash, session)

    assert change_result is True
    assert fetch_result is not False
    assert fetch_result.password_hash == new_hash
    assert non_existing_user is False
# existing user gets updated
# hash in DB changes
# function returns success
# non-existing user returns failure

def test_delete_user(session):
    user = UserData(email=EMAIL, password_hash=PASSWORD_HASH)
    create_user(user, session)

    delete_result = delete_user(EMAIL, session)
    fetch_result = get_user_by_email(EMAIL, session)
    non_existing_user = delete_user(wrong_email, session)

    assert fetch_result is False
    assert delete_result is True
    assert non_existing_user is False
# existing user gets removed from DB
# function returns success
# deleting non-existing user returns failure