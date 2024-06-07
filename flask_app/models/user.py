from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

class User:
    db_name = "gastroglide"

    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.password = data['password']
        self.email = data['email']
        self.full_name = data['full_name']
        self.address = data['address']
        self.city = data['city']
        self.postal_code = data['postal_code']
        self.phone = data['phone']
        self.preferred_payment_method = data['preferred_payment_method']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO users (username, password, email, full_name, address, city, postal_code, phone, preferred_payment_method, created_at, updated_at)
        VALUES (%(username)s, %(password)s, %(email)s, %(full_name)s, %(address)s, %(city)s, %(postal_code)s, %(phone)s, %(preferred_payment_method)s, NOW(), NOW());
        """
        return connectToMySQL(cls.db_name).query_db(query, data)
    


    @classmethod
    def validate_registration(cls, data):
        is_valid = True

        if len(data['username']) < 3:
            flash("Username must be at least 3 characters long.")
            is_valid = False

        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address.")
            is_valid = False

        if len(data['password']) < 6:
            flash("Password must be at least 6 characters long.")
            is_valid = False

        return is_valid
