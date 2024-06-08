from flask_app.config.mysqlconnection import connectToMySQL

class Dish:
    db_name = "gastroglide"

    def __init__(self, data):
        self.id = data['id']
        self.menu_id = data['menu_id']
        self.name = data['name']
        self.description = data.get('description')
        self.price = data['price']
        self.image_url = data.get('image_url')

    @classmethod
    def save(cls, data):
        query = "INSERT INTO dishes (menu_id, name, description, price, image_url) VALUES (%(menu_id)s, %(name)s, %(description)s, %(price)s, %(image_url)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_by_menu_id(cls, menu_id):
        query = "SELECT * FROM dishes WHERE menu_id = %(menu_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, {"menu_id": menu_id})
        return [cls(dish) for dish in results] if results else []

    @classmethod
    def get_by_id(cls, dish_id):
        query = "SELECT * FROM dishes WHERE id = %(dish_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, {"dish_id": dish_id})
        return cls(results[0]) if results else None

    @classmethod
    def update(cls, data):
        query = "UPDATE dishes SET name=%(name)s, description=%(description)s, price=%(price)s, image_url=%(image_url)s WHERE id=%(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete(cls, dish_id):
        query = "DELETE FROM dishes WHERE id = %(dish_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, {"dish_id": dish_id})
