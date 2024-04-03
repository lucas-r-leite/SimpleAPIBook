from flask import Flask, jsonify, request
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

# Define the MariaDB engine using MariaDB Connector/Python
engine = sqlalchemy.create_engine(
    "mariadb+mariadbconnector://root:ovLcA5^p8@localhost:3306/APILivros")

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

    return jsonify(bookList)


@app.route('/books/<int:id>', methods=['GET'])
def getBooksById(id):
    book = session.query(Books).filter_by(id=id).first()
    if book is None:
        return "Book not found", 404

    book_details = {"Title": book.title, "Author": book.author}
    return jsonify(book_details)


@app.route('/books/<int:id>', methods=['PUT'])
def updateBookById(id):
    book = session.query(Books).get(id)

    if book is None:
        return "Book not found", 404

    data = request.json  # Assuming JSON data is sent in the request body
    if 'title' in data:
        book.title = data['title']
    if 'author' in data:
        book.author = data['author']

    session.commit()

    return "Book updated successfully", 200


@app.route('/books/add', methods=['POST'])
def addNewBook():
    data = request.json
    title = data.get('title')
    author = data.get('author')

    if not title or not author:
        return "Title and author are required", 400

    newBook = Books(title=title, author=author)
    session.add(newBook)
    session.commit()

    return "Book added successfully", 201


@app.route('/books/delete/<int:id>', methods=['DELETE'])
def deleteBookById(id):
    book = session.query(Books).filter_by(id=id).first()
    if book is None:
        return "Book not found", 404

    session.delete(book)
    session.commit()

    return "Book deleted successfully", 200


app.run()
