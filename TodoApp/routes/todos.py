from fastapi import APIRouter, Depends, Path, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from models.models import Todos
from db.database import SessionLocal
from starlette import status
from request.todo_request import TodoRequest


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

@route.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependecy):
    return db.query(Todos).all()

@route.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependecy, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    else:
        raise HTTPException(status_code=404, detail="Todo not found")

@route.post("/todo/new", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependecy, todo: TodoRequest):
    todo_model = Todos(**todo.model_dump())
    try: 
        db.add(todo_model)
        db.commit()
        db.refresh(todo_model)
    except:
        raise HTTPException(status_code=400, detail="Somenthing went wrong, try again later")

@route.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependecy, todo_request: TodoRequest,  todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
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
async def delete_todo(db: db_dependecy, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    else:
        db.delete(todo_model)
        db.commit()
    

