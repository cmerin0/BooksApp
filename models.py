from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    description = Column(String)
    cover_url = Column(String)
    availability = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now(tz=timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(tz=timezone.utc), onupdate=datetime.now(tz=timezone.utc))

    def __repr__(self):
        return f"<Book {self.id}, title: '{self.title}', author: '{self.author}'>"

