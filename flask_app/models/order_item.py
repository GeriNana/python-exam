from flask_app.config.mysqlconnection import connectToMySQL

class OrderItem:
    db_name = "gastroglide"

    def __init__(self, data):
        self.id = data.get('id')
        self.order_id = data.get('order_id')
        self.menu_id = data.get('menu_id')
        self.dish_id = data.get('dish_id')
        self.quantity = data.get('quantity')
        self.price = data.get('price')

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO order_items (order_id, menu_id, dish_id, quantity, price)
        VALUES (%(order_id)s, %(menu_id)s, %(dish_id)s, %(quantity)s, %(price)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_by_order_id(cls, order_id):
        query = """
        SELECT * FROM order_items WHERE order_id = %(order_id)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query, {'order_id': order_id})
        order_items = []
        for result in results:
            order_items.append(cls(result))
        return order_items
