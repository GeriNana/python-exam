from flask_app.config.mysqlconnection import connectToMySQL

class OrderItem:
    db_name = "gastroglide"

    def __init__(self, data):
        self.id = data['id']
        self.order_id = data['order_id']
        self.menu_id = data['menu_id']
        self.quantity = data.get('quantity', 1)
        self.price = data.get('price', 0.0)

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO order_items (order_id, menu_id, quantity, price) 
        VALUES (%(order_id)s, %(menu_id)s, %(quantity)s, %(price)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_by_user_id(cls, user_id):
        query = """
        SELECT order_items.* FROM order_items
        JOIN orders ON order_items.order_id = orders.order_id
        WHERE orders.user_id = %(user_id)s;
        """
        print(f"Running Query: {query} with user_id: {user_id}")
        result = connectToMySQL(cls.db_name).query_db(query, {"user_id": user_id})
        
        if isinstance(result, list):
            print(f"Order items found: {result}")
            return [cls(row) for row in result]
        else:
            print(f"Query returned unexpected result: {result}")
            return []
