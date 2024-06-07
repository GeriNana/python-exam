from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class User:
    db_name = "gastroglide"

    def __init__(self, data):
        self.user_id = data['user_id']
        self.username = data['username']
        self.password = data['password']
        self.email = data['email']
        self.full_name = data['full_name']
        self.address = data['address']
        self.city = data['city']
        self.postal_code = data['postal_code']
        self.phone = data['phone']
        self.preferred_payment_method = data['preferred_payment_method']

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO users (username, password, email, full_name, address, city, postal_code, phone, preferred_payment_method) 
        VALUES (%(username)s, %(password)s, %(email)s, %(full_name)s, %(address)s, %(city)s, %(postal_code)s, %(phone)s, %(preferred_payment_method)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE user_id = %(user_id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return cls(result[0])
        return None

