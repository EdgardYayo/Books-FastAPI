from fastapi import APIRouter, Depends, Path, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from models.models import Todos
from db.database import SessionLocal
from starlette import status
from request.todo_request import TodoRequest
from .auth import get_current_user


route = APIRouter()

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

@route.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependecy):
    if user is None:
        raise HTTPException(status_code=401, detail='Authenticated Failed')
    
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()

@route.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependecy, 
                    todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authenticated Failed')
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id')).first()
    
    if todo_model is not None:
        return todo_model
    else:
        raise HTTPException(status_code=404, detail="Todo not found")

@route.post("/todo/new", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependecy, 
                      todo: TodoRequest):
    
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todo_model = Todos(**todo.model_dump(), owner_id=user.get('id'))
    try: 
        db.add(todo_model)
        db.commit()
        db.refresh(todo_model)
    except:
        raise HTTPException(status_code=400, detail="Somenthing went wrong, try again later")

@route.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependecy, 
                      todo_request: TodoRequest,  todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id')).first()
    
    if todo_model is not None:
        todo_model.title = todo_request.title
        todo_model.description = todo_request.description
        todo_model.priority = todo_request.priority
        todo_model.complete = todo_request.complete
        db.add(todo_model)
        db.commit()
        db.refresh(todo_model)
    else:
        raise HTTPException(status_code=404, detail="Todo not found")

@route.delete("/todo/delete/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, 
                      db: db_dependecy, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id')).first()
    
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    else:
        db.delete(todo_model)
        db.commit()
    

