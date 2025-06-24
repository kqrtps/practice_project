# dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from . import models
from .database import get_db

# Цей URL повинен збігатися з ендпоінтом login/token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Секретний ключ (той самий, який ти використовуєш у login)
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> models.User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user
