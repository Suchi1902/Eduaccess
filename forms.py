from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    TextAreaField,
    PasswordField,
    SubmitField
)

from wtforms.validators import DataRequired, Email

from flask_wtf.file import FileField



class RegisterForm(FlaskForm):

    username = StringField(
        "Username",
        validators=[DataRequired()]
    )


    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )


    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )


    submit = SubmitField(
        "Register"
    )




class LoginForm(FlaskForm):

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )


    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )


    submit = SubmitField(
        "Login"
    )





class CourseForm(FlaskForm):

    title = StringField(
        "Course Title",
        validators=[DataRequired()]
    )


    category = StringField(
        "Category",
        validators=[DataRequired()]
    )


    description = TextAreaField(
        "Description",
        validators=[DataRequired()]
    )


    link = StringField(
        "Course Link",
        validators=[DataRequired()]
    )


    image = FileField(
        "Course Image"
    )


    submit = SubmitField(
        "Add Course"
    )