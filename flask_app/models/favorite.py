from flask_app.config.mysqlconnection import connectToMySQL

class Favorite:
    db_name = "gastroglide"

    def __init__(self, data):
        self.id = data.get('id')
        self.user_id = data.get('user_id')
        self.menu_id = data.get('menu_id')
        self.dish_id = data.get('dish_id')
        self.dish_name = data.get('dish_name')
        self.restaurant_name = data.get('restaurant_name')

    @classmethod
    def add_favorite(cls, data):
        query = """
        INSERT INTO user_favorites (user_id, menu_id, dish_id) 
        VALUES (%(user_id)s, %(menu_id)s, %(dish_id)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_by_user_id(cls, user_id):
        query = """
        SELECT f.user_id, f.menu_id, f.dish_id, d.name AS dish_name, r.name AS restaurant_name
        FROM user_favorites f
        JOIN dishes d ON f.dish_id = d.id
        JOIN menus m ON d.menu_id = m.id
        JOIN restaurants r ON m.restaurant_id = r.restaurant_id  -- Corrected column name
        WHERE f.user_id = %(user_id)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query, {'user_id': user_id})
        if results:
            return [cls(result) for result in results]
        return []

    @classmethod
    def remove_favorite(cls, data):
        query = """
        DELETE FROM user_favorites
        WHERE user_id = %(user_id)s AND menu_id = %(menu_id)s AND dish_id = %(dish_id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)


    @classmethod
    def delete_by_dish_id(cls, dish_id):
        query = "DELETE FROM user_favorites WHERE dish_id = %(dish_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, {'dish_id': dish_id})