from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
# from flask_app.models.recipe import Recipe
from flask import flash
from flask_bcrypt import Bcrypt
import re
bcrypt = Bcrypt(app)

# Description	
# Email validation. With this short expression you can validate for proper email format. It's short and accurate.
# Matches	
# bob-smith@foo.com | bob.smith@foo.com | bob_smith@foo.com
# Non-Matches	
# -smith@foo.com | .smith@foo.com | smith@foo_com
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.recipes = []

    @classmethod
    def save_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        user_id = connectToMySQL("recipes").query_db(query, data)
        return user_id

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("recipes").query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validation(data):
        is_valid = True
        if len(data["first_name"])<2:
            flash("Name must be at least 1 characters.")
            is_valid = False
        if len(data["last_name"])<2:
            flash("Last name must be at least 2 characters")
            is_valid = False
        if not email_regex.match(data["email"]): 
            flash("Invalid email address!", "email")
            is_valid = False
        if len(data["password"])<1:
            flash("You must enter a password")
            is_valid = False
        if data["password"]!= data["confirm_pw"]:
            flash("passwords do not match!")
            is_valid = False
        return is_valid

    @staticmethod
    def login_validation(data):
        is_valid = True
        if not email_regex.match(data["log_in_email"]): 
            flash("Invalid email address!", "email")
            is_valid = False
        if len(data["log_in_password"])<1:
            flash("You must enter a password")
            is_valid = False
        return is_valid