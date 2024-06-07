from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class OrderItem:
    db_name = "gastroglide"

    def __init__(self, data):
        self.order_item_id = data['order_item_id']
        self.order_id = data['order_id']
        self.menu_id = data['menu_id']
        self.quantity = data['quantity']
        self.price = data['price']

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO order_items (order_id, menu_id, quantity, price) 
        VALUES (%(order_id)s, %(menu_id)s, %(quantity)s, %(price)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM order_items WHERE order_item_id = %(order_item_id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return cls(result[0])
        return None

    # Add more methods as needed
