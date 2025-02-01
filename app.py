from flask import Flask
from routes import books

# Initialize Flask app
app = Flask(__name__)

# Importing Books Routes 
app.register_blueprint(books)

# Routes
@app.route('/')
def index():
    return 'Welcome to the library!'

# Calling main function
if __name__ == '__main__':
    app.run(debug=True)