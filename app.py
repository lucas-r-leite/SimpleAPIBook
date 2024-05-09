from flask import Flask
from routes.books import book_route
from routes.home import home_route


app = Flask(__name__)

app.register_blueprint(home_route)
app.register_blueprint(book_route, url_prefix="/books")


if __name__ == "__main__":
    app.run()
