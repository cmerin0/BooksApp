# Simple Book App Installation Guide

## Project Purpose

The Simple Book App is designed to provide a straightforward API for managing a collection of books. It leverages several key technologies to ensure efficient and reliable operation:

- **PostgreSQL**: Serves as the primary database for storing book information.
- **Redis**: Acts as a cache to handle frequent requests and improve performance.
- **Flask**: Functions as the web server framework to handle API requests.
- **Gunicorn**: Utilized as the WSGI server to run the Flask application.
- **Nginx**: Configured as a reverse proxy to manage incoming traffic and provide SSL termination.

This setup ensures a robust and scalable environment for the book management API, making it easy to deploy and maintain.

## Prerequisites

This repository provides a simple setup to get your Docker Compose environment up and running.
Before you begin, ensure you have the following installed on your system:

- **Docker**: [Download Docker](https://www.docker.com/get-started)
- **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Setup Instructions

### 1. Clone the repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/cmerin0/Booksapp.git
cd BooksApp
```

### 2. Aplication structure

```
/db
    conn.py - Contains the database connection setup.
    examples.json - Sample data for populating the database.
    init.sql - SQL script for initializing the database schema.

/nginx
    nginx.conf - Configuration file for Nginx.
    /certs
        server.key - SSL certificate key.
        server.cert - SSL certificate file.

.env - Environment variables for the development environment.
.env.prod - Environment variables for the production environment.
app.py - Main application file for the Flask app.
docker-compose.yml - Docker Compose configuration file.
Dockerfile - Instructions to build the Docker image.
models.py - Database models for the application.
requirements.txt - List of Python dependencies.
routes.py - API route definitions.
wsgi.py - Entry point for the WSGI server.
```

### 3. Build and Run the application

Use Docker Compose to build and start services:

```bash
docker-compose up --build
```

This is going to start the following services:

* PostgreSQL as a database service exposing port 5432 internally
* Redis as a database cache service exposing port 6379 internally
* Flask application served in port 5000 internally, this, depending on healthy check of Postgres Service
* NginX proxy service as a reverse proxy in port 444 SSL in case you are already using 443 locally

To access the application visit:

```bash
https://localhost:443/
```

### 4. API Endpoints 

* **Get Books:** [GET /api/books] - Retrieves a list of all books.
* **Get a Book:** [GET /api/books/book_id] - Retrieves details of a specific book by its ID.
* **Insert Book:** [POST /api/books] - Adds a new book to the collection.
* **Update Book:** [PUT /api/books/book_id] - Updates the details of an existing book by its ID.
* **Delete Book:** [DELETE /api/books/book_id] - Deletes a book from the collection by its ID.

#### Body 

Example of the body fields

```json
{
    "title": "Don Quijote de la Mancha",
    "author": "Miguel de Cervantes",
    "description": "A story about a nobleman who loses his sanity from reading chivalric romances and decides to become a knight-errant.",
    "cover_url": "https://upload.wikimedia.org/wikipedia/commons/6/6f/Don_Quijote_and_Sancho_Panza.jpg",
    "availability": true
}
```

### 5. Stopping Application 

To stop application run

```bash
docker-compose down -v 
```

To remove the volumes created add **-v** flag, if you want to keep them, remove the **-v**