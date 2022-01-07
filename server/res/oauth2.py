from jose import jwt, JWTError
from datetime import datetime, timedelta
from flask import make_response, jsonify
from schemas.schemas import TokenDataSchema

#Secret Key
#Algorith
#Expiration time

SECRET_KEY = 'a0553cb8e8d497fd1fea5fb5798dbf9e8468cdd45dd166170bc8327ad82c637c'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

token_data_schema = TokenDataSchema()

def create_acces_token(data: dict):
  to_encode = data.copy()
  expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
  return encoded_jwt


def verify_token(token: str, credentials_exception):
  try:
    jwtData = token.split()[1]
    payload = jwt.decode(jwtData, SECRET_KEY, algorithms= [ALGORITHM])
    token_data = token_data_schema.dump(payload)
  except JWTError as e:
    print(e)
    resp = make_response({'error':str(e)}, 401,{'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'})
    return resp
  return token_data

def get_current_user(token: str):
  return verify_token(token, 'Could not validate credentials')
