from flask import Flask, request, render_template, url_for, redirect
import sqlalchemy
from dotenv import load_dotenv
import os
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

app = Flask(__name__)

# Define the MariaDB engine using MariaDB Connector/Python
engine = sqlalchemy.create_engine(
    f"mariadb+mariadbconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@localhost:3306/{os.getenv('DB_NAME')}")

Base = declarative_base()


class Books(Base):
    __tablename__ = 'books'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String(length=100))
    author = sqlalchemy.Column(sqlalchemy.String(length=50))


Base.metadata.create_all(engine)


Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()


@app.route('/books', methods=['GET'])
def getBooks():
    books = session.query(Books).all()
    bookList = []
    for book in books:
        bookList.append("Title: " + book.title + ' Author: ' + book.author)

    return render_template('books.html', books=books)


@app.route('/books/<int:id>', methods=['GET'])
def getBooksById(id):
    book = session.query(Books).filter_by(id=id).first()
    if book is None:
        return "Book not found", 404

    return render_template('bookDetails.html', book=book)


@app.route('/books/update/<int:id>', methods=['GET', 'POST'])
def updateBookById(id):
    book = session.query(Books).get(id)

    if book is None:
        return "Book not found", 404

    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')

        if not title or not author:
            return "Title and author are required", 400

        book.title = title
        book.author = author

        session.commit()

        return redirect(url_for('getBooksById', id=id))

    return render_template('updateBook.html', book=book)


@app.route('/books/add', methods=['GET', 'POST'])
def addNewBook():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')

        if not title or not author:
            return "Title and author are required", 400

        newBook = Books(title=title, author=author)
        session.add(newBook)
        session.commit()

        return redirect(url_for('getBooks'))

    return render_template('addBook.html')


@app.route('/books/delete/<int:id>', methods=['GET', 'POST'])
def deleteBookById(id):
    book = session.query(Books).filter_by(id=id).first()
    if book is None:
        return "Book not found", 404

    if request.method == 'POST':
        session.delete(book)
        session.commit()
        # Redirect to the book list page after deletion
        return redirect(url_for('getBooks'))

    # Render the delete confirmation page
    return render_template('deleteBook.html', book=book)


app.run()
