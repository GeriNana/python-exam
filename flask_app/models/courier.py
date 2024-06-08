from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Courier:
    db_name = "gastroglide"

    def __init__(self, data):
        self.courier_id = data['courier_id']
        self.full_name = data['full_name']
        self.phone = data['phone']
        self.email = data['email']
        self.status = data['status']

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO couriers (full_name, phone, email, status) 
        VALUES (%(full_name)s, %(phone)s, %(email)s, %(status)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM couriers WHERE courier_id = %(courier_id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return cls(result[0])
        return None


