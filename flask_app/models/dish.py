from flask_app.config.mysqlconnection import connectToMySQL

class Dish:
    db_name = "gastroglide"

    def __init__(self, data):
        self.id = data.get('id')
        self.menu_id = data.get('menu_id')
        self.name = data.get('name')
        self.description = data.get('description')
        self.price = data.get('price')
        self.image_url = data.get('image_url')

    @classmethod
    def get_by_id(cls, id):
        query = "SELECT * FROM dishes WHERE id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, {'id': id})
        if result:
            return cls(result[0])
        return None

    @classmethod
    def get_by_menu_id(cls, menu_id):
        query = "SELECT * FROM dishes WHERE menu_id = %(menu_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, {'menu_id': menu_id})
        dishes = []
        for result in results:
            dishes.append(cls(result))
        return dishes

    
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO dishes (menu_id, name, description, price, image_url) VALUES (%(menu_id)s, %(name)s, %(description)s, %(price)s, %(image_url)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE dishes SET name=%(name)s, description=%(description)s, price=%(price)s, image_url=%(image_url)s WHERE id=%(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete(cls, dish_id):
        query = "DELETE FROM dishes WHERE id = %(dish_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, {"dish_id": dish_id})
