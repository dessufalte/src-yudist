import uuid
from passlib.hash import bcrypt

def generate_id():
    new_uuid = uuid.uuid4()
    formatted_uuid = '-'.join([new_uuid.hex[:8], new_uuid.hex[8:12], new_uuid.hex[12:16], new_uuid.hex[16:20], new_uuid.hex[20:]])
    return formatted_uuid
def hash_password(password):
    hashed_password = bcrypt.hash(password)
    return hashed_password
def verify_password(hashed_password, input_password):
    return bcrypt.verify(input_password, hashed_password)
