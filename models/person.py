from ..extensions import db
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Person(UserMixin, db.Model, SerializerMixin):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(400), nullable=False)
