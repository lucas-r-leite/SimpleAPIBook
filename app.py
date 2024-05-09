from flask import Flask
from routes.books import book_route


app = Flask(__name__)


app.register_blueprint(book_route)


if __name__ == "__main__":
    app.run()
