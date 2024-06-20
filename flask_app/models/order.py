from flask_app.config.mysqlconnection import connectToMySQL

class Order:
    db_name = "gastroglide"

    def __init__(self, data):
        self.id = data.get('order_id')
        self.user_id = data.get('user_id')
        self.restaurant_id = data.get('restaurant_id')
        self.order_date = data.get('order_date')
        self.delivery_address = data.get('delivery_address')
        self.city = data.get('city')
        self.postal_code = data.get('postal_code')
        self.phone = data.get('phone')
        self.total_price = data.get('total_price')
        self.payment_method = data.get('payment_method')
        self.status = data.get('status')

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO orders (user_id, restaurant_id, order_date, delivery_address, city, postal_code, phone, total_price, payment_method, status)
        VALUES (%(user_id)s, %(restaurant_id)s, %(order_date)s, %(delivery_address)s, %(city)s, %(postal_code)s, %(phone)s, %(total_price)s, %(payment_method)s, %(status)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_by_user_id(cls, user_id):
        query = "SELECT * FROM orders WHERE user_id = %(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, {'user_id': user_id})
        orders = []
        for result in results:
            orders.append(cls(result))
        return orders

    @classmethod
    def get_by_order_id(cls, order_id):
        query = "SELECT * FROM orders WHERE order_id = %(order_id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, {'order_id': order_id})
        if result:
            return cls(result[0])
        return None
