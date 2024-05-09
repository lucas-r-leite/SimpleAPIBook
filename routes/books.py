from flask import request, render_template, url_for, redirect, Blueprint
import sys
import mariadb
from dotenv import load_dotenv
import os

load_dotenv()


book_route = Blueprint("book", __name__)

# Database configuration
DATABASE_HOST = "0.0.0.0"  # Replace with the IP of your MariaDB container
DATABASE_USER = os.getenv("DB_USER")
DATABASE_PASSWORD = os.getenv("DB_PASSWORD")
DATABASE_DB = os.getenv("DB_NAME")


# Connect to MariaDB
try:
    conn = mariadb.connect(
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=3306,  # MariaDB default port
        database=DATABASE_DB,
    )
    cursor = conn.cursor()
except mariadb.Error as e:
    print(f"Error connecting to MariaDB: {e}")
    sys.exit(1)

# Define the Books table creation SQL query
CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    author VARCHAR(30) NOT NULL
)
"""

# Execute the table creation query
try:
    cursor.execute(CREATE_TABLE_QUERY)
    conn.commit()
    print("Books table created successfully.")
except mariadb.Error as e:
    print(f"Error creating Books table: {e}")
    conn.rollback()


@book_route.route("/books", methods=["GET"])
def getBooks():
    try:
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
        return render_template("books/books.html", books=books)
    except mariadb.Error as e:
        print(f"Error fetching books: {e}")
        return "Error fetching books", 500


@book_route.route("/books/<int:id>", methods=["GET"])
def getBooksById(id):
    try:
        cursor.execute("SELECT * FROM books WHERE id=?", (id,))
        book = cursor.fetchone()
        if not book:
            return "Book not found", 404
        return render_template("books/bookDetails.html", book=book)
    except mariadb.Error as e:
        print(f"Error retrieving book: {e}")
        return "Error retrieving book", 500


@book_route.route("/books/update/<int:id>", methods=["GET", "POST"])
def updateBookById(id):
    try:
        cursor.execute("SELECT * FROM books WHERE id=?", (id,))
        book = cursor.fetchone()
        if not book:
            return "Book not found", 404

        if request.method == "POST":
            title = request.form.get("title")
            author = request.form.get("author")

            if not title or not author:
                return "Title and author are required", 400

            cursor.execute(
                "UPDATE books SET title=?, author=? WHERE id=?", (
                    title, author, id)
            )
            conn.commit()

            return redirect(url_for("getBooksById", id=id))

        return render_template("books/updateBook.html", book=book)
    except mariadb.Error as e:
        print(f"Error updating book: {e}")
        return "Error updating book", 500


@book_route.route("/books/add", methods=["GET", "POST"])
def addNewBook():
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")

        if not title or not author:
            return "Title and author are required", 400

        try:
            cursor.execute(
                "INSERT INTO books (title, author) VALUES (?, ?)", (title, author)
            )
            conn.commit()
            return redirect(url_for("getBooks"))
        except mariadb.Error as e:
            print(f"Error adding new book: {e}")
            return "Error adding new book", 500

    return render_template("books/addBook.html")


@book_route.route("/books/delete/<int:id>", methods=["GET", "POST"])
def deleteBookById(id):
    try:
        cursor.execute("SELECT * FROM books WHERE id=?", (id,))
        book = cursor.fetchone()
        if not book:
            return "Book not found", 404

        if request.method == "POST":
            cursor.execute("DELETE FROM books WHERE id=?", (id,))
            conn.commit()
            return redirect(url_for("getBooks"))

        return render_template("books/deleteBook.html", book=book)
    except mariadb.Error as e:
        print(f"Error deleting book: {e}")
        return "Error deleting book", 500
