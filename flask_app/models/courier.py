from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
from flask_app import app

bcrypt = Bcrypt(app)

class Courier:
    def __init__(self, data):
        self.id = data.get('id')
        self.full_name = data.get('full_name')
        self.email = data.get('email')
        self.phone = data.get('phone')
        self.address = data.get('address')
        self.city = data.get('city')
        self.postal_code = data.get('postal_code')
        self.vehicle_type = data.get('vehicle_type')
        self.password = data.get('password')
        self.confirmed = data.get('confirmed')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO couriers (full_name, email, phone, address, city, postal_code, vehicle_type, password, confirmed, created_at, updated_at)
        VALUES (%(full_name)s, %(email)s, %(phone)s, %(address)s, %(city)s, %(postal_code)s, %(vehicle_type)s, %(password)s, %(confirmed)s, NOW(), NOW())
        ON DUPLICATE KEY UPDATE
        full_name = VALUES(full_name),
        phone = VALUES(phone),
        address = VALUES(address),
        city = VALUES(city),
        postal_code = VALUES(postal_code),
        vehicle_type = VALUES(vehicle_type),
        password = VALUES(password),
        confirmed = VALUES(confirmed),
        updated_at = NOW();
        """
        return connectToMySQL('gastroglide').query_db(query, data)

    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM couriers WHERE email = %(email)s;"
        data = {'email': email}
        result = connectToMySQL('gastroglide').query_db(query, data)
        if result:
            return cls(result[0])
        return None

    @classmethod
    def get_by_id(cls, courier_id):
        query = "SELECT * FROM couriers WHERE id = %(id)s;"
        data = {'id': courier_id}
        result = connectToMySQL('gastroglide').query_db(query, data)
        if result:
            return cls(result[0])
        return None

    @classmethod
    def update_password(cls, email, password):
        query = "UPDATE couriers SET password = %(password)s WHERE email = %(email)s;"
        data = {'email': email, 'password': password}
        connectToMySQL('gastroglide').query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = """
        UPDATE couriers
        SET full_name = %(full_name)s, email = %(email)s, phone = %(phone)s, address = %(address)s, city = %(city)s, postal_code = %(postal_code)s, vehicle_type = %(vehicle_type)s, password = %(password)s, confirmed = %(confirmed)s, updated_at = NOW()
        WHERE id = %(id)s;
        """
        connectToMySQL('gastroglide').query_db(query, data)
    
    @classmethod
    def delete(cls, courier_id):
        query = "DELETE FROM couriers WHERE id = %(id)s;"
        data = {'id': courier_id}
        connectToMySQL('gastroglide').query_db(query, data)
