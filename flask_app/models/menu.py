from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.dish import Dish

class Menu:
    db_name = "gastroglide"

    def __init__(self, data):
        self.id = data['id']
        self.restaurant_id = data['restaurant_id']
        self.image_url = data.get('image_url')
        self.restaurant_name = data.get('restaurant_name')
        self.min_order_amount = data.get('min_order_amount')
        self.avg_preparation_time = data.get('avg_preparation_time')
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
        return [cls(result) for result in results]

    @classmethod
    def get_by_id(cls, menu_id):
        query = "SELECT * FROM menus WHERE id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, {"id": menu_id})
        if result:
            menu = cls(result[0])
            menu.dishes = Dish.get_by_menu_id(menu_id)
            return menu
        return None

    @classmethod
    def update(cls, data):
        query = """
        UPDATE menus
        SET image_url = %(image_url)s, restaurant_name = %(restaurant_name)s, min_order_amount = %(min_order_amount)s, avg_preparation_time = %(avg_preparation_time)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete(cls, menu_id):
        query = "DELETE FROM menus WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, {"id": menu_id})
