from flask_app.config.mysqlconnection import connectToMySQL

class Order:
    db = "gastroglide"

    def __init__(self, data):
        self.order_id = data['order_id']
        self.user_id = data['user_id']
        self.restaurant_name = data['restaurant_name']
        self.order_date = data['order_date']
        self.total_price = data['total_price']
        self.dishes = data['dishes']

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
        if results:
            orders = []
            for row in results:
                order = {
                    'order_id': row['order_id'],
                    'user_id': row['user_id'],
                    'restaurant_name': row['restaurant_name'],
                    'order_date': row['order_date'],
                    'total_price': row['total_price'],
                    'dishes': row['dishes']
                }
                orders.append(order)
            return orders
        return []

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO orders (user_id, restaurant_id, order_date, delivery_address, city, postal_code, phone, total_price, payment_method, status) 
        VALUES (%(user_id)s, %(restaurant_id)s, %(order_date)s, %(delivery_address)s, %(city)s, %(postal_code)s, %(phone)s, %(total_price)s, %(payment_method)s, %(status)s);
        """
        return connectToMySQL(cls.db).query_db(query, data)
