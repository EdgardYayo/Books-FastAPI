from fastapi import FastAPI, Depends, Path, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
import models.models
from models.models import Todos
from db.database import engine, SessionLocal
from starlette import status
from request.todo_request import TodoRequest

app = FastAPI()

models.models.Base.metadata.create_all(bind=engine)

#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependecy =  Annotated[Session, Depends(get_db)]

@app.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependecy):
    return db.query(Todos).all()

@app.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependecy, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    else:
        raise HTTPException(status_code=404, detail="Todo not found")

@app.post("/todo/new", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependecy, todo: TodoRequest):
    todo_model = Todos(**todo.model_dump())
    try: 
        db.add(todo_model)
        db.commit()
        db.refresh(todo_model)
    except:
        raise HTTPException(status_code=400, detail="Somenthing went wrong, try again later")
