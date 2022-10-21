from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

"""flask app wrapper for Flask
"""
app = Flask(__name__)

"""Configuration for Flask database
"""
DIR_DB = "movies.db"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DIR_DB}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

"""Creation of the database for Flask
"""
db = SQLAlchemy(app)

"""Creation of the Api
"""
api = Api(
    app=app,
    version="1.0",
    title="FLASK | FLASK-RESTX",
    description=("This is a web api using FLASK-RESTX powered by rondweb@gmail.com"),
)
