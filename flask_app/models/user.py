from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PASWORD_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    db = "sighting"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            return cls(result[0])
        return None
    
    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            return cls(result[0])
        return None
        
    
    @classmethod
    def create(cls, data):
        print("Creating user with data:", data)  # Debugging statement
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query, data)



    @staticmethod
    def validate_user(user):
        is_valid = True
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'emailLogin')
            is_valid = False
        if len(user['password'])<1:
            flash("Password is required!", 'passwordLogin')
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_login(user):
        is_valid = True
        if len(user['email']) < 1:
            flash('Email is required', 'login')
            is_valid = False
        if len(user['password']) < 1:
            flash('Password is required', 'login')
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_userRegister(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters", 'nameRegister')
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters", 'lastNameRegister')
            is_valid = False
        if len(user['email']) < 1:
            flash("Email cannot be blank", 'emailRegister')
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", 'passwordRegister')
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords must match", 'confirmPasswordRegister')
            is_valid = False
        return is_valid
