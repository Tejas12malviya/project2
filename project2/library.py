from fastapi import FastAPI,Body
from pydantic import Field,BaseModel

class book:
    id:int
    title:str
    description:str
    price:float
    rating:float

    def __init__(self,id,title,description,price,rating):
        self.id=id
        self.title=title
        self.description=description
        self.price=price
        self.rating=rating

class bookRequest(BaseModel):
    id:int=Field(le=10,ge=1)
    
books=[
    book(1,"The God of Small Things","Arundhati Roy",499,4.5),
    book(2,"Midnight's Children","Salman Rushdie",599,4.8),
    book(3,"The White Tiger","Aravind Adiga",399,4.2),
    book(4,"Interpreter of Maladies","Jhumpa Lahiri",299,4.0),
    book(5,"The Inheritance of Loss","Kiran Desai",499,4.3)
]


app=FastAPI()

@app.get("/read_all")
def read_book():
    return books

@app.get("/read_book/{book_id}")
def read_book(book_id:int):
    for Book in books:
        if Book.id==book_id:
            return Book