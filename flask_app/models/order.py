from flask_app.config.mysqlconnection import connectToMySQL

class Order:
    db_name = "gastroglide"

    def __init__(self, data):
        self.order_id = data['order_id']
        self.user_id = data['user_id']
        self.restaurant_id = data['restaurant_id']
        self.order_date = data['order_date']
        self.delivery_address = data['delivery_address']
        self.city = data['city']
        self.postal_code = data['postal_code']
        self.phone = data['phone']
        self.total_price = data['total_price']
        self.payment_method = data['payment_method']
        self.status = data['status']

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO orders (user_id, restaurant_id, order_date, delivery_address, city, postal_code, phone, total_price, payment_method, status) 
        VALUES (%(user_id)s, %(restaurant_id)s, %(order_date)s, %(delivery_address)s, %(city)s, %(postal_code)s, %(phone)s, %(total_price)s, %(payment_method)s, %(status)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM orders WHERE order_id = %(order_id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return cls(result[0])
        return None
