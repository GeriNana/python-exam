from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.dish import Dish

class Menu:
    db_name = "gastroglide"

    def __init__(self, data):
        self.id = data['id']
        self.restaurant_id = data['restaurant_id']
        self.image_url = data.get('image_url')
        self.restaurant_name = data['restaurant_name']
        self.min_order_amount = data['min_order_amount']
        self.avg_preparation_time = data['avg_preparation_time']
        self.dishes = []

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO menus (restaurant_id, image_url, restaurant_name, min_order_amount, avg_preparation_time)
        VALUES (%(restaurant_id)s, %(image_url)s, %(restaurant_name)s, %(min_order_amount)s, %(avg_preparation_time)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_by_restaurant_id(cls, restaurant_id):
        query = "SELECT * FROM menus WHERE restaurant_id = %(restaurant_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, {"restaurant_id": restaurant_id})
        menus = []
        for menu in results:
            menus.append(cls(menu))
        return menus

    @classmethod
    def get_by_id(cls, menu_id):
        query = "SELECT * FROM menus WHERE id = %(menu_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, {"menu_id": menu_id})
        if len(results) < 1:
            return None
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = """
        UPDATE menus SET image_url=%(image_url)s, restaurant_name=%(restaurant_name)s, min_order_amount=%(min_order_amount)s, avg_preparation_time=%(avg_preparation_time)s 
        WHERE id=%(id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete(cls, menu_id):
        query = "DELETE FROM menus WHERE id = %(menu_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, {"menu_id": menu_id})
