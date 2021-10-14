from re import U
from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    if not User.validation(request.form):
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    print(pw_hash)
    data = {
        "first_name":request.form["first_name"],
        "last_name":request.form["last_name"],
        "email":request.form["email"],
        "password":pw_hash,
        "confirm_pw":request.form["confirm_pw"]
    }
    
    new_user = User.save_user(data)
    flash("User Created!")
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    if not User.login_validation(request.form):
        return redirect("/")
    data = {
        "email": request.form["log_in_email"]
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form["log_in_password"]):
        flash("Invalid Email/Password")
        return redirect('/')

    # REMEMBER!! If you update(edit) a name in a call you need to update the session var too!    
    session["user_id"] = user_in_db.id
    session["first_name"] = user_in_db.first_name
    session["logged_in"] = True
    session["email"] = user_in_db.email   
    return redirect("/dashboard")


@app.route("/logout")
def logout():
    session.clear()
    flash("log out succesful")
    return redirect("/")



