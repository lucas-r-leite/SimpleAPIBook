from flask import Flask
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


# Create a session
Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()


@app.route('/books', methods=['GET'])
def getBooks():
    books = session.query(Books).all()
    for book in books:
        print(" - " + book.title + ' ' + book.author)


@app.route('/books/<int:id>', methods=['GET'])
def getBooksById(id):
    books = session.query(Books).filter_by(id=id)
    for book in books:
        print(" - " + book.title + ' ' + book.author)


@app.route('/books/<int:id>', methods=['PUT'])
def updateBookById(id, title, author):
    book = session.query(Books).get(id)
    if book is None:
        # Return a 404 Not Found status if the book doesn't exist
        return "Book not found", 404
    else:
        book.title = title
        book.author = author

    session.commit()


@app.route('/books/add', methods=['POST'])
def addNewBook(title, author):
    newBook = Books(title=title, author=author)
    session.add(newBook)
    session.commit()


@app.route('/books/delete/<int:id>', methods=['DELETE'])
def deleteBookById(id):
    session.query(Books).filter(Books.id == id).delete()
    session.commit()


# add new book
# addNewBook("Narnia", "C. S. Lewis")
print("----------------")

# add new book
# updateBookById(3, "Nárnia", "C. S. Lewis")
# print("----------------")


# Show all books
print('All books')
getBooks()
print("----------------")

# deleteBookById(1)

app.run()
