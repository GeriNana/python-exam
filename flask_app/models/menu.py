from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Menu:
    db_name = "gastroglide"

    def __init__(self, data):
        self.menu_id = data['menu_id']
        self.restaurant_id = data['restaurant_id']
        self.name = data['name']
        self.description = data['description']
        self.price = data['price']
        self.image_url = data['image_url']

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO menus (restaurant_id, name, description, price, image_url) 
        VALUES (%(restaurant_id)s, %(name)s, %(description)s, %(price)s, %(image_url)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM menus WHERE menu_id = %(menu_id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return cls(result[0])
        return None

    # Add more methods as needed
