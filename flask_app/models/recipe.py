from werkzeug.datastructures import ImmutableTypeConversionDict
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt


class Recipe:
    def __init__(self, data):
        self.id = data["id"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.recipes = data["recipes"]
        self.user_id = data["user_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.under_thirty = data["under_thirty"]
        self.date_made = data["date_made"]
        self.recipe = []

    @classmethod
    def insert_recipe(cls, data):
        query = "INSERT INTO recipes (description, instructions, recipes, user_id, under_thirty, date_made) VALUES (%(description)s, %(instructions)s, %(recipes)s, %(user_id)s, %(under_thirty)s, %(date_made)s)"
        return connectToMySQL("recipes").query_db(query, data)

    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET description = %(description)s, instructions = %(instructions)s, recipes = %(recipes)s, user_id = %(id)s, under_thirty = %(under_thirty)s, date_made = %(date_made)s WHERE recipes.user_id = %(id)s"
        return connectToMySQL("recipes").query_db(query, data)

    @classmethod
    def delete_recipe(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s"
        return connectToMySQL("recipes").query_db(query,data)

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL("recipes").query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_recipes(cls):
        query = "SELECT * FROM recipes"
        recipes_thirty_db = connectToMySQL("recipes").query_db(query)
        recipes_thirty =[]
        for r in recipes_thirty_db:
            recipe_instance = Recipe(r)
            recipes_thirty.append(recipe_instance)
        return recipes_thirty

    @classmethod
    def join_users_recipes(cls):
        query = "SELECT * FROM users JOIN ON users.id = recipes.user_id"
        recipes_thirty_db = connectToMySQL("recipes").query_db(query)
        user_recipes =[]
        for r in recipes_thirty_db:
            user_instance = User(r)
            recipe_data = {
                "id":r["recipes.id"],
                "description":r["description"],
                "instructions":r["instructions"],
                "recipes":r["recipes"],
                "user_id":r["user.id"],
                "created_at":r["created_at"],
                "updated_at":r["updated_at"],
                "under_thirty":r["under_thirty"],
                "date_made":r["date_made"]
            }
            user_instance.recipe = Recipe(recipe_data)
            user_recipes.append(user_instance)
        return user_recipes

    @classmethod
    def join_oneuser_recipes(cls,data):
        query = "SELECT * FROM users JOIN recipes ON users.id = recipes.user_id WHERE recipes.id = %(id)s"
        user_recipes_db = connectToMySQL("recipes").query_db(query,data)
        user_recipe = Recipe(user_recipes_db[0])
        for r in user_recipes_db:
            recipe_data = {
                "id":r["recipes.id"],
                "description":r["description"],
                "instructions":r["instructions"],
                "recipes":r["recipes"],
                "user_id":r["user_id"],
                "created_at":r["created_at"],
                "updated_at":r["updated_at"],
                "under_thirty":r["under_thirty"],
                "date_made":r["date_made"]
            }
            user_recipe.recipe.append(Recipe(recipe_data))
        return user_recipe



    @staticmethod
    def validate_recipe(data):
        print(data)
        is_valid = True
        if len(data["recipes"])<2:
            flash("Recipe must be at least 1 characters.")
            is_valid = False
        if len(data["description"])<2:
            flash("Description must be at least 2 characters")
            is_valid = False
        if len(data["instructions"])<2:
            flash("You must enter some instruction!")
            is_valid = False
        if len(data["date_made"])<1:
            flash("You must enter a valid date!")
            is_valid = False
        if  "under_thirty" not in data:
            flash("please select if this dish can be made in under 30 minutes")
            is_valid = False
        return is_valid