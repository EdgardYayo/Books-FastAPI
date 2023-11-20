from fastapi import APIRouter, Depends, Path, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from models.models import Todos, Users
from db.database import SessionLocal
from starlette import status
from .auth import get_current_user


route = APIRouter(
     prefix='/admin',
     tags=['admin']
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


@route.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependecy):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Todos).all()

@route.get("/users", status_code=status.HTTP_200_OK)
async def all_users(user: user_dependency, db: db_dependecy):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Users).all()

@route.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user: user_dependency, db: db_dependecy, user_id: int = Path(gt=0)):
     if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
     
     user_model = db.query(Users).filter(Users.id == user_id).first()
     if user_model is None:
         raise HTTPException(status_code=404, detail='User not found')
     db.delete(user_model)
     db.commit()