from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Restaurant:
    db_name = "gastroglide"

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.address = data['address']
        self.city = data['city']
        self.postal_code = data['postal_code']
        self.phone = data['phone']
        self.email = data['email']
        self.logo_url = data['logo_url']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO restaurants (name, address, city, postal_code, phone, email, logo_url, created_at, updated_at) VALUES (%(name)s, %(address)s, %(city)s, %(postal_code)s, %(phone)s, %(email)s, %(logo_url)s, NOW(), NOW());"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_by_location(cls, location):
        query = "SELECT * FROM restaurants WHERE city = %(location)s;"
        results = connectToMySQL(cls.db_name).query_db(query, {'location': location})
        restaurants = []
        for row in results:
            restaurants.append(cls(row))
        return restaurants
