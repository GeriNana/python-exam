from flask_app.config.mysqlconnection import connectToMySQL

class Menu:
    def __init__(self, data):
        self.id = data['menu_id']
        self.restaurant_id = data['restaurant_id']
        self.name = data['name']
        self.description = data.get('description')
        self.price = data['price']
        self.image_url = data.get('image_url')

    @classmethod
    def save(cls, data):
        query = "INSERT INTO menus (restaurant_id, name, description, price, image_url) VALUES (%(restaurant_id)s, %(name)s, %(description)s, %(price)s, %(image_url)s);"
        return connectToMySQL('gastroglide').query_db(query, data)
    
    @classmethod
    def get_by_restaurant_id(cls, restaurant_id):
        query = "SELECT * FROM menus WHERE restaurant_id = %(restaurant_id)s;"
        results = connectToMySQL('gastroglide').query_db(query, {"restaurant_id": restaurant_id})
        return [cls(menu) for menu in results] if results else []
