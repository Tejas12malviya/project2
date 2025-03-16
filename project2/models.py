from databse import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey

class User(Base):
    __tablename__='Users'

    id=Column(Integer,primary_key=True,index=True)
    email=Column(String,unique=True)
    user_name=Column(String,unique=True)
    first_name=Column(String)
    last_name=Column(String)
    hashed_password=Column(String)
    is_active=Column(Boolean,default=True)

class Todo(Base):
    __tablename__='todos'

    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    description=Column(String)
    priority=Column(Integer)
    completed=Column(Boolean,default=False)
    user_id=Column(Integer,ForeignKey(User.id))