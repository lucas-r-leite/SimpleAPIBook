from flask import request, render_template, url_for, redirect, Blueprint
import mariadb
from db import conn, cursor


book_route = Blueprint("book", __name__)


@book_route.route("/", methods=["GET"])
def getBooks():
    try:
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
        return render_template("books/books.html", books=books)
    except mariadb.Error as e:
        print(f"Error fetching books: {e}")
        return "Error fetching books", 500


@book_route.route("/<int:id>", methods=["GET"])
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


@book_route.route("/update/<int:id>", methods=["GET", "POST"])
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

            return redirect(url_for("book.getBooks"))

        return render_template("books/updateBook.html", book=book)
    except mariadb.Error as e:
        print(f"Error updating book: {e}")
        return "Error updating book", 500


@book_route.route("/add", methods=["GET", "POST"])
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
            return redirect(url_for("book.getBooks"))
        except mariadb.Error as e:
            print(f"Error adding new book: {e}")
            return "Error adding new book", 500

    return render_template("books/addBook.html")


@book_route.route("/delete/<int:id>", methods=["GET", "POST"])
def deleteBookById(id):
    try:
        cursor.execute("SELECT * FROM books WHERE id=?", (id,))
        book = cursor.fetchone()
        if not book:
            return "Book not found", 404

        if request.method == "POST":
            cursor.execute("DELETE FROM books WHERE id=?", (id,))
            conn.commit()
            return redirect(url_for("book.getBooks"))

        return render_template("books/deleteBook.html", book=book)
    except mariadb.Error as e:
        print(f"Error deleting book: {e}")
        return "Error deleting book", 500
