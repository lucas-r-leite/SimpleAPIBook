from routes.books import book_route
from routes.home import home_route


def configureRoutes(app):
    app.register_blueprint(home_route)
    app.register_blueprint(book_route, url_prefix="/books")
