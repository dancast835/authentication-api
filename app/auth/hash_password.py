from passlib.hash import bcrypt

def secure_password(password):
    h = bcrypt.hash(password)
    return h

def verify_password(plain_password, stored_hash):
    verified = bcrypt.verify(plain_password, stored_hash)
    if verified:
        return True
    else:
        return False