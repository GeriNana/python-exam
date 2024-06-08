from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class CourierApplication:
    db_name = "gastroglide"

    def __init__(self, data):
        self.application_id = data['application_id']
        self.courier_id = data['courier_id']
        self.application_date = data['application_date']
        self.status = data['status']

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO courier_applications (courier_id, application_date, status) 
        VALUES (%(courier_id)s, %(application_date)s, %(status)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM courier_applications WHERE application_id = %(application_id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return cls(result[0])
        return None
