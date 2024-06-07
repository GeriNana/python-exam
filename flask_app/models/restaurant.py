from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Restaurant:
    db_name = "gastroglide"

    def __init__(self, data):
        self.restaurant_id = data['restaurant_id']
        self.name = data['name']
        self.address = data['address']
        self.city = data['city']
        self.postal_code = data['postal_code']
        self.phone = data['phone']
        self.email = data['email']
        self.logo_url = data['logo_url']  # Add the logo_url attribute

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO restaurants (name, address, city, postal_code, phone, email, logo_url) 
        VALUES (%(name)s, %(address)s, %(city)s, %(postal_code)s, %(phone)s, %(email)s, %(logo_url)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM restaurants WHERE restaurant_id = %(restaurant_id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return cls(result[0])
        return None

    # Add more methods as needed
