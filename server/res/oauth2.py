from jose import jwt, JWTError
from datetime import datetime, timedelta

#Secret Key
#Algorith
#Expiration time

SECRET_KEY = 'a0553cb8e8d497fd1fea5fb5798dbf9e8468cdd45dd166170bc8327ad82c637c'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_acces_token(data: dict):
  to_encode = data.copy()
  expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
  return encoded_jwt