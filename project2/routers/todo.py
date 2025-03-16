from fastapi import Depends,HTTPException,Path,APIRouter
from starlette import status
from pydantic import BaseModel,Field
from databse import SessionLocal
from models import Todo
from typing import Annotated
from sqlalchemy.orm import Session

router=APIRouter()

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]

class TodoRequest(BaseModel):
    title:str
    description:str
    priority:int=Field(le=5,ge=1)
    completed:bool


@router.get('/')
def read_all(db:db_dependency):
    return db.query(Todo).all()

@router.get('/{id}',status_code=status.HTTP_200_OK)
def read_by_id(db:db_dependency,id:int=Path(ge=0)):
    todo_model= db.query(Todo).filter(Todo.id==id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404,detail='Todo not found')

@router.post('/create',status_code=status.HTTP_200_OK)
def create_file(db:db_dependency,todo_request:TodoRequest):
    todo_model=Todo(**todo_request.dict())
    db.add(todo_model)
    db.commit()
    return todo_model

@router.put('/update_todo/{todo_id}',status_code=status.HTTP_200_OK)
def updated_file(db:db_dependency,
                 todo_id:int,
                 todo_request:TodoRequest):
    todo_model=db.query(Todo).filter(Todo.id==todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404,detail='Todo not found.')
    todo_model.title=todo_request.title
    todo_model.description=todo_request.description
    todo_model.priority=todo_request.priority
    todo_model.completed=todo_request.completed

    db.add(todo_model)
    db.commit()

@router.delete('/todo_delete/{todo_id}')
def delete_todo(db:db_dependency,todo_id:int):
    todo_model=db.query(Todo).filter(Todo.id==todo_id).first()
    if todo_model is None :
        raise HTTPException(status_code=404,detail='Todo not founnd')
    db.query(Todo).filter(Todo.id==todo_id).delete()
    db.commit()
    return {"message":"Todo deleted successfully"}
