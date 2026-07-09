from flask import Flask, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from models import db, User
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        print("✅ Form is valid")

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

    # Print validation errors in terminal
    if form.errors:
        print("❌ Form Errors:", form.errors)

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):
            flash("Login successful!", "success")
            return redirect(url_for("home"))

        flash("Invalid email or password!", "danger")

    if form.errors:
        print("❌ Login Form Errors:", form.errors)

    return render_template("login.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)