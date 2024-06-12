from flask_app.config.mysqlconnection import connectToMySQL

class UserPastOrder:
    db = "gastroglide"

    def __init__(self, data):
        self.user_id = data['user_id']
        self.order_id = data['order_id']

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO user_past_orders (user_id, order_id) 
        VALUES (%(user_id)s, %(order_id)s);
        """
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM user_past_orders WHERE user_id = %(user_id)s AND order_id = %(order_id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            return cls(result[0])
        return None

    @classmethod
    def get_by_user_id(cls, user_id):
        query = """
            SELECT o.order_id, o.user_id, r.name AS restaurant_name, o.order_date, o.total_price,
                   GROUP_CONCAT(d.name SEPARATOR ', ') AS dishes
            FROM orders o
            JOIN restaurants r ON o.restaurant_id = r.restaurant_id
            JOIN order_items oi ON o.order_id = oi.order_id
            JOIN dishes d ON oi.dish_id = d.id
            WHERE o.user_id = %(user_id)s
            GROUP BY o.order_id;
        """
        results = connectToMySQL(cls.db).query_db(query, {'user_id': user_id})
        return [cls(result) for result in results] if results else []
