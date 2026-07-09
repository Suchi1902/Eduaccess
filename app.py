from flask import Flask, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from config import Config
from models import db, User, Course
from forms import RegisterForm, LoginForm, CourseForm

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        existing_user = User.query.filter_by(email=form.email.data).first()

        if existing_user:
            flash("Email already exists!", "danger")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(form.password.data)

        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.", "success")

        return redirect(url_for("login"))

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)

            flash("Login successful!", "success")

            return redirect(url_for("dashboard"))

        flash("Invalid email or password!", "danger")

    return render_template("login.html", form=form)


@app.route("/dashboard")
@login_required
def dashboard():

    courses = Course.query.filter_by(created_by=current_user.id).all()

    return render_template(
        "dashboard.html",
        courses=courses
    )


@app.route("/add-course", methods=["GET", "POST"])
@login_required
def add_course():

    form = CourseForm()

    if form.validate_on_submit():

        course = Course(
            title=form.title.data,
            category=form.category.data,
            description=form.description.data,
            link=form.link.data,
            created_by=current_user.id
        )

        db.session.add(course)
        db.session.commit()

        flash("Course added successfully!", "success")

        return redirect(url_for("dashboard"))

    return render_template("add_course.html", form=form)


@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Logged out successfully.", "success")

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)