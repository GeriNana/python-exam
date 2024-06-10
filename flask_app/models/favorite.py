from flask_app.config.mysqlconnection import connectToMySQL

class Favorite:
    db_name = "gastroglide"

    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.menu_id = data['menu_id']

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO user_favorites (user_id, menu_id) 
        VALUES (%(user_id)s, %(menu_id)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_by_user_id(cls, user_id):
        query = "SELECT * FROM user_favorites WHERE user_id = %(user_id)s;"
        print(f"Running Query: {query} with user_id: {user_id}")
        result = connectToMySQL(cls.db_name).query_db(query, {"user_id": user_id})
        
        if isinstance(result, list):
            print(f"Favorites found: {result}")
            return [cls(row) for row in result]
        else:
            print(f"Query returned unexpected result: {result}")
            return []
