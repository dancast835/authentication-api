from passlib.hash import bcrypt
from app.auth.hash_password import secure_password, verify_password



def test_secure_password():
    #arrange
    plain_password = "Hello123!"

    #act
    hashed_password = secure_password(plain_password)

    #assert
    assert isinstance(hashed_password, str)
    assert hashed_password != plain_password

    # Possible failures:
    # returns the original password
    # returns None
    # accepts wrong password as valid
    
def test_verify_password():
    plain_password = "Hello123!"

    hashed_password = secure_password(plain_password)

    verified = verify_password(plain_password, hashed_password)

    assert verified == True


    #possible failures:
    #returns False
    







