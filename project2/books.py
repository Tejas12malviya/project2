from fastapi import FastAPI,Body

Book = [
    {"name": "The God of Small Things", "author": "Arundhati Roy", "genre": "Fiction", "price": 499},
    {"name": "Midnight's Children", "author": "Salman Rushdie", "genre": "Historical Fiction", "price": 599},
    {"name": "The White Tiger", "author": "Aravind Adiga", "genre": "Fiction", "price": 399},
    {"name": "Interpreter of Maladies", "author": "Jhumpa Lahiri", "genre": "Short Stories", "price": 299},
    {"name": "A Suitable Boy", "author": "Vikram Seth", "genre": "Fiction", "price": 699},
    {"name": "The Inheritance of Loss", "author": "Kiran Desai", "genre": "Fiction", "price": 499},
    {"name": "Train to Pakistan", "author": "Khushwant Singh", "genre": "Historical Fiction", "price": 349},
    {"name": "The Palace of Illusions", "author": "Chitra Banerjee Divakaruni", "genre": "Mythology", "price": 399},
    {"name": "The Immortals of Meluha", "author": "Amish Tripathi", "genre": "Mythology", "price": 350},
    {"name": "Shantaram", "author": "Gregory David Roberts", "genre": "Fiction", "price": 599}
]

app=FastAPI()

@app.get("/")
def book():
    return("Welcome to the Books API")

@app.get("/Books")
async def read_books():
    return Book

@app.get("/Books/{book_name}")
def book_name(book_name):
    for book in Book:
        if book.get('name').casefold()==book_name.casefold():
            return book
        
@app.get("/Books/")
def read_book(price:int):
    for book in Book:
        if book.get("price")==price:
            return book
        

@app.post('/Books')
def add_book(new_book=Body()):
    Book.append(new_book)
    return Book

@app.put("/Books/")
def update_book(updated_Book=Body()):
    for i in range (len(Book)):
        if Book[i].get('name')==updated_Book.get('name'):
            Book[i]=updated_Book
            return Book[i]
        
@app.delete("/Books/{book_name}")
def delete_book(book_name):
    for i in range(len(Book)):
        if Book[i].get('name')==book_name:
            del Book[i]
            return Book
 
 