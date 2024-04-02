from flask import Flask, jsonify, request

app = Flask(__name__)

books = [
    {
        'id': 1,
        'title': 'The Lord of Rings',
        'author': 'J.R.R Tolkien'
    },
    {
        'id': 2,
        'title': 'Harry Potter',
        'author': 'J.K. Howling'
    },
    {
        'id': 3,
        'title': 'James Clear',
        'author': 'Hábitos Atômicos'
    },
]


@app.route('/books', methods=['GET'])
def getBooks():
    return jsonify(books)


@app.route('/books/<int:id>', methods=['GET'])
def getBooksById(id):
    for book in books:
        if book.get('id') == id:
            return jsonify(book)


@app.route('/books/<int:id>', methods=['PUT'])
def updateBookById(id):
    updatedBook = request.get_json()
    for index, book in enumerate(books):
        if book.get('id') == id:
            books[index].update(updatedBook)
            return jsonify(books[index])


@app.route('/books/add', methods=['POST'])
def addNewBook():
    newBook = request.get_json()
    books.append(newBook)

    return jsonify(books)


@app.route('/books/delete/<int:id>', methods=['DELETE'])
def deleteBookById(id):
    for index, book in enumerate(books):
        if book.get('id') == id:
            del books[index]

            return jsonify(books)


app.run(debug=True)
