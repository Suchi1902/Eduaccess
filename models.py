from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(200), nullable=False)

    courses = db.relationship("Course", backref="author", lazy=True)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), nullable=False)

    category = db.Column(db.String(100), nullable=False)

    description = db.Column(db.Text, nullable=False)

    link = db.Column(db.String(300), nullable=False)

    created_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)