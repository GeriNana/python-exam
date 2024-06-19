from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.order_item import OrderItem

def calculate_total_price(order_id):
    order_items = OrderItem.get_by_order_id(order_id)

    total_price = sum(item.price * item.quantity for item in order_items)
    
    return total_price


def insert_order(user_id, total_price, delivery_address, postal_code, phone, payment_method, restaurant_id):
    query = """
    INSERT INTO orders (user_id, total_price, delivery_address, postal_code, phone, payment_method, status, restaurant_id)
    VALUES (%(user_id)s, %(total_price)s, %(delivery_address)s, %(postal_code)s, %(phone)s, %(payment_method)s, 'Pending', %(restaurant_id)s);
    """
    data = {
        'user_id': user_id,
        'total_price': total_price,
        'delivery_address': delivery_address,
        'postal_code': postal_code,
        'phone': phone,
        'payment_method': payment_method,
        'restaurant_id': restaurant_id
    }
    result = connectToMySQL('gastroglide').query_db(query, data)
    return result

def get_past_orders(user_id):
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
    data = {'user_id': user_id}
    result = connectToMySQL('gastroglide').query_db(query, data)
    return result
