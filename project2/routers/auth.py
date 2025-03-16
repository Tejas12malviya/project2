# from fastapi import FastAPI

# app=FastAPI()   

# @app.get("/")
# def auth():
#     return{'User':'Authenticated'}

# To run above auth.py file we need different port terminal and run uvicorn auth:app --reload

# But we can use APIROUTER to run multiple files in same terminal by connecting their endpoints to main.py file

from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import session
from typing import Annotated
from starlette import status
from pydantic import BaseModel,Field
from models import User
from passlib.context import CryptContext
from databse import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from datetime import timedelta,datetime,timezone

class UserRequest(BaseModel):
    email:str
    user_name:str
    first_name:str
    last_name:str
    password:str
    is_active:bool


router=APIRouter()

SECREAT_KEY='db6e7c3bf96f99a5d23445d799e0f1e1f79b09500b5714353d8fb53e8a81133d'
ALGORITHM='HS256'

bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

def auth(username:str,password:str,db):
    user=db.query(User).filter(User.user_name==username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.hashed_password):
        return False
    return user
    


db_dependency=Annotated[session,Depends(get_db)]
request_form=Annotated[OAuth2PasswordRequestForm,Depends()]

def create_access_token(username:str,user_id:int,expire_delta=timedelta):
    encode={'sub':username,'id':user_id}
    expire=datetime.now(timezone.utc)+expire_delta
    encode.update({'exp':expire})
    return jwt.encode(encode,SECREAT_KEY,algorithm=ALGORITHM)

@router.post('/User_Autentication')
def User_Authentication(form:request_form,db:db_dependency):
    user_model=auth(form.username,form.password,db)
    if not user_model:
        return 'User Authentication Failed'
    
    token=create_access_token(user_model.user_name,user_model.id,timedelta(minutes=20))
    return token


@router.post("/User")
def create_user(db:db_dependency,
                user_request:UserRequest):
    # user_model=User(**user_request.dict())  -----> This do not run because in UserRequest we are using password but in models.User we have hashed password so we need to create them seperately
    create_user_model=User(
        email=user_request.email,
        user_name=user_request.user_name,
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        is_active=user_request.is_active,
        hashed_password=bcrypt_context.hash(user_request.password)
    )

    db.add(create_user_model)
    db.commit()
    return create_user_model

@router.get("/User")
def read_user(db:db_dependency):
    user_model=db.query(User).all()
    return user_model

# @router.get("User/{User_name}")
# def read_user(db:db_dependency, 
#               User_name:str,
#               password:str):
#     user_model=db.query(User).filter(User.user_name==User_name & User.hashed_password==bcrypt_context.hash(password))
#     return user_model

@router.put('/update_user/{user_id}')
def update_user(db:db_dependency,
                user_id:int,
                user_request:UserRequest):
    user_model=db.query(User).filter(User.id==user_id).first()
    if user_model is None:
        raise HTTPException(status_code=404,detail='User not found')
    user_model.user_name=user_request.user_name