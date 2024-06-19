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

class CourierApplication:
    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM courier_applications WHERE email = %s"
        results = connectToMySQL('gastroglide').query_db(query, (email,))
        if len(results) < 1:
            return False
        return cls(results[0])

class Courier:
    @classmethod
    def save(cls, data):
        query = "INSERT INTO couriers (full_name, email, phone, address, city, postal_code, vehicle_type, password) VALUES (%(full_name)s, %(email)s, %(phone)s, %(address)s, %(city)s, %(postal_code)s, %(vehicle_type)s, %(password)s)"
        return connectToMySQL('gastroglide').query_db(query, data)

    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM couriers WHERE email = %s"
        results = connectToMySQL('gastroglide').query_db(query, (email,))
        if len(results) < 1:
            return False
        return cls(results[0])
