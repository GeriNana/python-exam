from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class UserPastOrder:
    db_name = "gastroglide"

    def __init__(self, data):
        self.user_id = data['user_id']
        self.order_id = data['order_id']

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO user_past_orders (user_id, order_id) 
        VALUES (%(user_id)s, %(order_id)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM user_past_orders WHERE user_id = %(user_id)s AND order_id = %(order_id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return cls(result[0])
        return None

    # Add more methods as needed
