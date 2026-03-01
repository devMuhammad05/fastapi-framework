import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone

ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY="d4472e9744f681fe3ff784f194c684f2b830216a00af6ae100ebffa90911c0c2"
ALGORITHM="HS256"

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    