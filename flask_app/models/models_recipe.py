from flask_app.config.mysqlconnection import connectToMySQL
# Flash messages import
from flask import flash
from flask_app.models import models_user

# Database name
db = "recipes_schema"

# Recipe class
class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.cook_time = data['cook_time']
        self.date_made = data['date_made']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # Classmethod for saving a recipe.
    @classmethod
    def save_recipe(cls, data):
        print("Saving Recipe...")
        query = """INSERT INTO recipes (name, description, instructions,
                cook_time, date_made, user_id) VALUES (%(name)s, %(description)s,
                %(instructions)s, %(cook_time)s, %(date_made)s, %(user_id)s);"""
        print("Recipe successfully saved...")
        return connectToMySQL(db).query_db(query, data)

    # Classmethod for getting all the recipes.
    @classmethod
    def get_all_recipes(cls):
        print("Getting all the recipes...")
        query = """SELECT * FROM recipes JOIN users on
                users.id  = recipes.user_id;"""
        results = connectToMySQL(db).query_db(query)
        all_recipes = []
        for row in results:
            recipe = cls(row)
            posting_user = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            recipe.user = models_user.User(posting_user)
            all_recipes.append(recipe)
        print("Successfully gathered all recipes...")
        return all_recipes

    # Classmethod for getting one recipe.
    @classmethod
    def get_one_recipe(cls, data):
        print("Getting the recipe...")
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        print("Recipe aquired...")
        return cls(results[0])

    # Classmethod for updating the recipe.
    @classmethod
    def update_recipe(cls, data):
        print("Updating the recipe...")
        query = """UPDATE recipes SET name=%(name)s, description=%(description)s,
                instructions=%(instructions)s, cook_time=%(cook_time)s, date_made=%(date_made)s,
                updated_at=NOW() WHERE id = %(id)s;"""
        print("Recipe update successful...")
        return connectToMySQL(db).query_db(query, data)

    # Classmethod for deleting a recipe.
    @classmethod
    def destroy_recipe(cls, data):
        print("Deleting the recipe...")
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        print("Deletion successful...")
        return connectToMySQL(db).query_db(query, data)

    # Staticmethod for validating a recipe.
    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            is_valid = False
            flash("Name must be at least 3 characters", "recipe")
        if len(recipe['description']) < 3:
            is_valid = False
            flash("Description must be at least 3 characters", "recipe")
        if len(recipe['instructions']) < 3:
            is_valid = False
            flash("Instructions must be at least 3 characters", "recipe")
        if recipe['date_made'] == "":
            is_valid = False
            flash("Please enter a date", "recipe")
        # if recipe['cook_time'] == "":
        #     is_valid = False
        #     flash("Please give a cook time", "recipe")
        return is_valid