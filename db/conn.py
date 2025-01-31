from models import Base, Book
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import json
import os

# Load environment variables from .env file
load_dotenv()

# Create database connection
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)

# Create tables from the model
Base.metadata.create_all(engine)

# Creating session
Session = sessionmaker(bind=engine)
session = Session()

"""
def insert_books(books_data):
    for book in books_data:
        book = Book(
            title=book['title'],
            author=book['author'],
            description=book['description'],
            cover_url=book['cover_url'],
            availability=book['availability']
        )
        session.add(book)

    session.commit()
    session.close()
    print("Books inserted succesfully!")

# Open Json File 
with open('db/examples.json') as file:
    books = json.load(file)
    insert_books(books)
"""