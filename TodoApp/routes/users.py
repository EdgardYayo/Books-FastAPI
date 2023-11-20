from fastapi import APIRouter, Depends, Path, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from models.models import Users
from db.database import SessionLocal
from starlette import status
from .auth import get_current_user
from request.user_verification import UserVerification
from passlib.context import CryptContext


route = APIRouter(
     prefix='/users',
     tags=['users']
)

#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Dependency Injection
db_dependecy =  Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

# Setting the bcrypt context to hash password
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

@route.get("/profile", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependecy):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    return db.query(Users).filter(Users.id == user.get('id')).first()


@route.put("/new_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependecy,
                          user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    
    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')

    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()
    db.refresh(user_model)