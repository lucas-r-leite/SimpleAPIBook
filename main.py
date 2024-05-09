from flask import Flask
from config import configureRoutes

app = Flask(__name__)

configureRoutes(app)

if __name__ == "__main__":
    app.run()
