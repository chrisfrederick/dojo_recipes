from re import U
import re
from flask_app import app
from flask import render_template, redirect, request, session
import flask_app
from flask_app.models.recipe import Recipe
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/dashboard")
def dashboard():
    if "logged_in" not in session:
        flash("Not Logged In")
        return redirect("/")
    get_recipes_thirty = Recipe.get_recipes()
    return render_template("dashboard.html", get_recipes_thirty = get_recipes_thirty)

@app.route("/add_recipe")
def add_recipe():
    if "logged_in" not in session:
        flash("Not Logged In")
        return redirect("/")
    return render_template("add_recipe.html")

@app.route("/insert_recipe", methods=["POST"])
def insert_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect("/dashboard")
    data = {
        "recipes":request.form["recipes"],
        "description":request.form["description"],
        "instructions":request.form["instructions"],
        "user_id":session["user_id"],
        "under_thirty":request.form["under_thirty"],
        "date_made":request.form["date_made"]
    }
    Recipe.insert_recipe(data)
    flash("recipe added!")
    return redirect("/add_recipe")

@app.route("/oneuser_recipes/<int:id>")
def insert_oneuser_recipes(id):
        data = {
            "id":id,
        }
        user_recipes = Recipe.join_oneuser_recipes(data)
        return render_template("recipe.html", user_recipes=user_recipes)

@app.route("/edit_get/<int:id>")
def edit_recipe(id):
    data = {
        "id":id,
    }
    user = Recipe.get_by_id(data)
    return render_template("edit.html", user=user)

@app.route("/update_recipe/<int:id>", methods=["POST"])
def update_recipe(id):
    if "logged_in" not in session:
        flash("Not Logged In")
        return redirect("/")
    if Recipe.validate_recipe(request.form):
        data = {
            "recipes":request.form["recipes"],
            "description":request.form["description"],
            "instructions":request.form["instructions"],
            "id":session["user_id"],
            "under_thirty":request.form["under_thirty"],
            "date_made":request.form["date_made"],
        }
        Recipe.update_recipe(data)
        flash("recipe edited!")
        return redirect("/dashboard")
    else: 
        return redirect(f"/edit_get/{id}")

@app.route("/delete/<int:id>")
def delete(id):
    data = {
        "id":id
    }
    Recipe.delete_recipe(data)
    flash("Entry has been deleted")
    return redirect("/dashboard")
