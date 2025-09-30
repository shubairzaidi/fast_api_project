from requests import Session
from fastapi.security import HTTPBearer
from src.database.models import User
from src.database.session import get_db
from src.dependencies.auth import verify_token
from fastapi import Depends, HTTPException, status, Request

bearer_scheme = HTTPBearer()

def get_current_user(credentials = Depends(bearer_scheme), db: Session = Depends(get_db)):
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid or expired token")

    user_id = payload.get("sub")
    # If you store user id as int in the token, convert accordingly
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        raise HTTPException(status_code=401, detail="Token does not contain a valid user id")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
