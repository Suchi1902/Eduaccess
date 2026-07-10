from flask import Flask, render_template, redirect, url_for, flash, request
import os

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from config import Config
from models import db, User, Course,Favorite
from forms import (
    RegisterForm,
    LoginForm,
    CourseForm,
    UpdateProfileForm,
    ChangePasswordForm
)


app = Flask(__name__)
app.config.from_object(Config)

app.config["UPLOAD_FOLDER"] = Config.UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "gif"
}


db.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"



def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )



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

        existing_user = User.query.filter_by(
            email=form.email.data
        ).first()


        if existing_user:

            flash(
                "Email already exists!",
                "danger"
            )

            return redirect(
                url_for("register")
            )


        hashed_password = generate_password_hash(
            form.password.data
        )


        new_user = User(

            username=form.username.data,

            email=form.email.data,

            password=hashed_password

        )


        db.session.add(new_user)

        db.session.commit()


        flash(
            "Registration successful! Please login.",
            "success"
        )


        return redirect(
            url_for("login")
        )


    return render_template(
        "register.html",
        form=form
    )




@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()


    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()


        if user and check_password_hash(
            user.password,
            form.password.data
        ):


            login_user(user)


            flash(
                "Login successful!",
                "success"
            )


            return redirect(
                url_for("dashboard")
            )


        flash(
            "Invalid email or password!",
            "danger"
        )


    return render_template(
        "login.html",
        form=form
    )




@app.route("/dashboard")
@login_required
def dashboard():


    search = request.args.get("search")

    category = request.args.get("category")


    query = Course.query.filter_by(
        created_by=current_user.id
    )


    if search:

        query = query.filter(
            Course.title.ilike(
                f"%{search}%"
            )
        )


    if category and category != "All":

        query = query.filter(
            Course.category == category
        )


    courses = query.all()



    categories = (
        db.session.query(Course.category)
        .filter_by(created_by=current_user.id)
        .distinct()
        .all()
    )


    categories = [
        c[0]
        for c in categories
    ]


    return render_template(
        "dashboard.html",
        courses=courses,
        categories=categories,
        search=search,
        category=category
    )




@app.route("/add-course", methods=["GET", "POST"])
@login_required
def add_course():


    form = CourseForm()



    if form.validate_on_submit():


        filename = None


        if form.image.data:


            image = form.image.data


            if allowed_file(image.filename):


                filename = secure_filename(
                    image.filename
                )


                image.save(
                    os.path.join(
                        app.config["UPLOAD_FOLDER"],
                        filename
                    )
                )



        course = Course(

            title=form.title.data,

            category=form.category.data,

            description=form.description.data,

            link=form.link.data,

            image=filename,

            created_by=current_user.id

        )


        db.session.add(course)

        db.session.commit()


        flash(
            "Course added successfully!",
            "success"
        )


        return redirect(
            url_for("dashboard")
        )


    return render_template(
        "add_course.html",
        form=form
    )




@app.route("/edit-course/<int:course_id>", methods=["GET", "POST"])
@login_required
def edit_course(course_id):


    course = Course.query.get_or_404(
        course_id
    )


    if course.created_by != current_user.id:

        flash(
            "You are not authorized.",
            "danger"
        )

        return redirect(
            url_for("dashboard")
        )



    form = CourseForm()


    form.submit.label.text = "Update Course"



    if form.validate_on_submit():


        course.title = form.title.data

        course.category = form.category.data

        course.description = form.description.data

        course.link = form.link.data



        if form.image.data:


            image = form.image.data


            if allowed_file(image.filename):


                filename = secure_filename(
                    image.filename
                )


                image.save(
                    os.path.join(
                        app.config["UPLOAD_FOLDER"],
                        filename
                    )
                )


                course.image = filename



        db.session.commit()


        flash(
            "Course updated successfully!",
            "success"
        )


        return redirect(
            url_for("dashboard")
        )



    form.title.data = course.title

    form.category.data = course.category

    form.description.data = course.description

    form.link.data = course.link



    return render_template(
        "edit_course.html",
        form=form
    )




@app.route("/delete-course/<int:course_id>")
@login_required
def delete_course(course_id):


    course = Course.query.get_or_404(
        course_id
    )


    if course.created_by != current_user.id:

        flash(
            "You are not authorized.",
            "danger"
        )

        return redirect(
            url_for("dashboard")
        )


    db.session.delete(course)

    db.session.commit()


    flash(
        "Course deleted successfully!",
        "success"
    )


    return redirect(
        url_for("dashboard")
    )
@app.route("/profile")
@login_required
def profile():

    course_count = Course.query.filter_by(
        created_by=current_user.id
    ).count()


    return render_template(
        "profile.html",
        user=current_user,
        course_count=course_count
    )
@app.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():

    form = UpdateProfileForm()

    if form.validate_on_submit():

        current_user.username = form.username.data
        current_user.email = form.email.data

        db.session.commit()

        flash("Profile updated successfully!", "success")

        return redirect(url_for("profile"))

    form.username.data = current_user.username
    form.email.data = current_user.email

    return render_template(
        "edit_profile.html",
        form=form
    )

@app.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():

    form = ChangePasswordForm()

    if form.validate_on_submit():

        if not check_password_hash(
            current_user.password,
            form.current_password.data
        ):
            flash("Current password is incorrect!", "danger")
            return redirect(url_for("change_password"))

        current_user.password = generate_password_hash(
            form.new_password.data
        )

        db.session.commit()

        flash("Password changed successfully!", "success")

        return redirect(url_for("profile"))

    return render_template(
        "change_password.html",
        form=form
    )    




@app.route("/logout")
@login_required
def logout():


    logout_user()


    flash(
        "Logged out successfully.",
        "success"
    )


    return redirect(
        url_for("home")
    )




if __name__ == "__main__":

    app.run(debug=True)