from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class UserFavorite:
    db_name = "gastroglide"

    def __init__(self, data):
        self.user_id = data['user_id']
        self.menu_id = data['menu_id']

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO user_favorites (user_id, menu_id) 
        VALUES (%(user_id)s, %(menu_id)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM user_favorites WHERE user_id = %(user_id)s AND menu_id = %(menu_id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return cls(result[0])
        return None

    # Add more methods as needed
