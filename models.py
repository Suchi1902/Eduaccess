from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()


class User(db.Model, UserMixin):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )


    courses = db.relationship(
        "Course",
        backref="creator",
        lazy=True
    )



class Course(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    title = db.Column(
        db.String(200),
        nullable=False
    )


    category = db.Column(
        db.String(100),
        nullable=False
    )


    description = db.Column(
        db.Text,
        nullable=False
    )


    link = db.Column(
        db.String(500),
        nullable=False
    )


    image = db.Column(
        db.String(300)
    )


    created_by = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )