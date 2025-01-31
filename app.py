from flask import Flask, request, jsonify
from models import Book
from db.conn import session
from datetime import datetime, timezone
from dotenv import load_dotenv
import os
import redis
import logging

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Setting up Logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Setting up Redis connection
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:9736/0')
redis_client = redis.Redis.from_url(REDIS_URL)

# Helper function to get a cache key
def get_cache_key(endpoint, book_id=None):
    if book_id:
        return f'{endpoint}:{book_id}'
    return endpoint

# Routes
@app.route('/')
def index():
    return 'Welcome to the library!'

# Get many method route
@app.route('/api/books', methods=['GET'])
def get_books():
    try:
        cache_key = get_cache_key('get_books')
        cached_data = redis_client.get(cache_key)

        if cached_data:
            #data = cached_data.decode('utf-8').replace("'", '"') # Works with decode only but still have to pass to json
            return jsonify({'data': eval(cached_data), 'source': 'cache'})

        books = session.query(Book).all()
        books_data = [{
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'description': book.description,
            'cover_url': book.cover_url,
            'availability': book.availability
        } for book in books]

        redis_client.setex(cache_key, 60, str(books_data)) # Cache for 60 seconds
        return jsonify({'data': books_data, 'source': 'database'})
    except Exception as e:
        logger.error(f"Error in get_books(): {e}")
        return jsonify({"Error": "An Error occurred while fetching books" }), 500

# Get one method route
@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    try:
        cache_key = get_cache_key('get_book', book_id)
        cache_data = redis_client.get(cache_key)

        if cache_data:
            return jsonify({'data': eval(cache_data), 'source': 'cache'})

        book = session.query(Book).filter_by(id=book_id).first()
        if book:
            book_data = {
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'description': book.description,
                'cover_url': book.cover_url,
                'availability': book.availability
            }
            redis_client.setex(cache_key, 60, str(book_data)) # Cache for 60 seconds
            return jsonify({'data': book_data, 'source': 'database'})
        
        return jsonify({'message': 'Book not found'}), 404
    
    except Exception as e:
        logger.error(f"Error in get_book(): {e}")
        return jsonify({"Error": "An Error occurred while fetching a book" }), 500

# Insert method route
@app.route('/api/books', methods=['POST'])
def create_book():
    try:
        data = request.json
        new_book = Book(
            title=data['title'],
            author=data['author'],
            description=data['description'],
            cover_url=data['cover_url'],
            availability=data['availability']
        )
        session.add(new_book)
        session.commit()

        redis_client.delete(get_cache_key('get_books')) # Clear cache
        return jsonify({ 'message': 'Book created successufully', 'ID': new_book.id }), 201
    
    except Exception as e:
        session.rollback()
        logger.error(f"Error in create_book(): {e}")
        return jsonify({"Error": "An Error occurred while creating a book" }), 500

# Update method route 
@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    try:
        book = session.query(Book).filter_by(id=book_id).first()

        if not book:
            return jsonify({'message': 'Book not found'}), 404

        data = request.json
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.description = data.get('description', book.description)
        book.cover_url = data.get('cover_url', book.cover_url)
        book.availability = data.get('availability', book.availability)
        book.updated_at = datetime.now(tz=timezone.utc)
        session.commit()

        # Invalidate cache for get_book and get_books
        redis_client.delete(get_cache_key('get_books'))
        redis_client.delete(get_cache_key('get_book', book_id))

        return jsonify({ 'message': 'Book updated successully', 'Book': book.title })

    except Exception as e:
        session.rollback()
        logger.error(f"Error in create_book(): {e}")
        return jsonify({"Error": "An Error occurred while updating a book" }), 500

# Delete method route 
@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    try:
        book = session.query(Book).filter_by(id=book_id).first()
        if not book:
            return jsonify({'message': 'Book not found'}), 404
        
        session.delete(book)
        session.commit()

        # Invalidate cache for get_book and get_books
        redis_client.delete(get_cache_key('get_books'))
        redis_client.delete(get_cache_key('get_book', book_id))

        return jsonify({ 'message': 'Book Deleted successfully', 'ID': book.id })

    except Exception as e:
        session.rollback()
        logger.error(f"Error in delete_book(): {e}")
        return jsonify({"Error": "An Error occurred while deleting a book" }), 500

# Calling main function
if __name__ == '__main__':
    app.run(debug=True)