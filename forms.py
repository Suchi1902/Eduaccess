from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    TextAreaField,
    PasswordField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo
)

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
        validators=[
            DataRequired(),
        Length(min=6)
    ]
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
class UpdateProfileForm(FlaskForm):

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

    submit = SubmitField("Update Profile")  
class ChangePasswordForm(FlaskForm):

    current_password = PasswordField(
        "Current Password",
        validators=[DataRequired()]
    )

    new_password = PasswordField(
        "New Password",
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )

    confirm_password = PasswordField(
        "Confirm New Password",
        validators=[
            DataRequired(),
            EqualTo("new_password")
        ]
    )

    submit = SubmitField("Change Password")      