from Banco_de_dados.app import db
from Banco_de_dados.database import db # type: ignore
from flask_login import UserMixin # type: ignore

class User(db.Model, UserMixin):
    # id (inteiro), username (texto) , senha (texto)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.string(80), nullable=False, unique=True)
    password = db.Column(db.string(80), nullable=False)
