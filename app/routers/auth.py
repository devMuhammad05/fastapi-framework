from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import engine, get_db
from typing import Annotated

router = APIRouter(
    tags=['Authentication']
)


@router.post('/login')
def login(
    user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Invalid Credentials"
            )       
    
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Invalid Credentials"
            )   

    access_token = oauth2.create_access_token(data={"user_id":user.id})

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "Bearer token"
        }
