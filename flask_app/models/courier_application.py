from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from flask_app.config.mysqlconnection import connectToMySQL

class CourierApplication:
    def __init__(self, data):
        self.id = data['id']
        self.full_name = data['full_name']
        self.email = data['email']
        self.phone = data['phone']
        self.address = data['address']
        self.city = data['city']
        self.postal_code = data['postal_code']
        self.vehicle_type = data['vehicle_type']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO courier_applications (full_name, email, phone, address, city, postal_code, vehicle_type, created_at, updated_at) 
        VALUES (%(full_name)s, %(email)s, %(phone)s, %(address)s, %(city)s, %(postal_code)s, %(vehicle_type)s, NOW(), NOW());
        """
        return connectToMySQL('gastroglide').query_db(query, data)

    @classmethod
    def generate_confirmation_token(cls, email):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])

    @classmethod
    def confirm_token(cls, token, expiration=3600):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            email = serializer.loads(token, salt=current_app.config['SECURITY_PASSWORD_SALT'], max_age=expiration)
        except:
            return False
        return email

    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM courier_applications WHERE email = %(email)s;"
        data = {'email': email}
        result = connectToMySQL('gastroglide').query_db(query, data)
        if result:
            return cls(result[0])
        return None
