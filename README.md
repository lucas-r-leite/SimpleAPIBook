# Simple Book API with Flask

This is a simple RESTful API built with Flask to manage a collection of books.

## Endpoints

- **GET /books**: Retrieve all books.
- **GET /books/<id>**: Retrieve a specific book by ID.
- **PUT /books/update/<id>**: Update a specific book by ID.
- **POST /books/add**: Add a new book.
- **DELETE /books/delete/<id>**: Delete a specific book by ID.

## Security

For security reasons, sensitive variables such as database credentials should not be hardcoded directly into the codebase of a web application. Instead, they should be stored securely outside of the source code. In this project, I've used a .env file to store these sensitive variables.

The .env file contains environment variables such as database username, password, and database name. These variables are loaded into the Flask application using the python-dotenv library. By storing sensitive information in the .env file, we prevent it from being exposed in the source code or accidentally committed to version control.

Using environment variables in this manner enhances the security of the application by keeping sensitive information separate from the codebase. It also allows for easier configuration management, as variables can be updated in the .env file without modifying the source code.
