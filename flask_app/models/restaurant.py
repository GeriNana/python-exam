from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.menu import Menu

class Restaurant:
    db_name = "gastroglide"

    def __init__(self, data):
        self.id = data['restaurant_id']
        self.name = data['name']
        self.address = data.get('address')
        self.city = data.get('city')
        self.postal_code = data.get('postal_code')
        self.phone = data.get('phone')
        self.email = data['email']
        self.menus = []

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO restaurants (name, address, city, postal_code, phone, email)
        VALUES (%(name)s, %(address)s, %(city)s, %(postal_code)s, %(phone)s, %(email)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_by_id(cls, restaurant_id):
        query = "SELECT * FROM restaurants WHERE restaurant_id = %(restaurant_id)s;"
        data = {"restaurant_id": restaurant_id}
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if not result:
            return None
        restaurant = cls(result[0])
        restaurant.menus = cls.get_menus(restaurant_id)
        return restaurant

    @classmethod
    def get_menus(cls, restaurant_id):
        query = "SELECT * FROM menus WHERE restaurant_id = %(restaurant_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, {"restaurant_id": restaurant_id})
        menus = []
        for menu in results:
            menus.append(Menu(menu))
        return menus

    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM restaurants WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query, {'email': email})
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_location(cls, location):
        query = "SELECT * FROM restaurants WHERE city = %(location)s;"
        results = connectToMySQL(cls.db_name).query_db(query, {"location": location})
        return [cls(result) for result in results]

    def get_average_preparation_time(self):
        if not self.menus:
            return None
        total_time = sum(menu.avg_preparation_time for menu in self.menus if menu.avg_preparation_time)
        return total_time // len(self.menus) if self.menus else 0

    def get_min_order_amount(self):
        if not self.menus:
            return None
        min_order = min(menu.min_order_amount for menu in self.menus if menu.min_order_amount)
        return min_order if self.menus else 0

    @staticmethod
    def validate_registration(form_data):
        is_valid = True
        errors = []

        # Check name length
        if len(form_data['name']) < 2:
            is_valid = False
            errors.append("Name must be at least 2 characters.")

        # Check if email is valid and unique
        if 'email' not in form_data or not form_data['email']:
            is_valid = False
            errors.append("Email is required.")
        else:
            email_query = "SELECT * FROM restaurants WHERE email = %(email)s;"
            email_data = {"email": form_data['email']}
            email_results = connectToMySQL('gastroglide').query_db(email_query, email_data)
            if len(email_results) > 0:
                is_valid = False
                errors.append("Email is already in use.")

        # Check if phone number is provided
        if 'phone' not in form_data or not form_data['phone']:
            is_valid = False
            errors.append("Phone number is required.")

        # Check address length
        if 'address' in form_data and form_data['address'] and len(form_data['address']) < 5:
            is_valid = False
            errors.append("Address must be at least 5 characters.")

        # Check city length
        if 'city' in form_data and form_data['city'] and len(form_data['city']) < 2:
            is_valid = False
            errors.append("City must be at least 2 characters.")

        # Check postal code length
        if 'postal_code' in form_data and form_data['postal_code'] and len(form_data['postal_code']) < 3:
            is_valid = False
            errors.append("Postal code must be at least 3 characters.")

        if not is_valid:
            for error in errors:
                flash(error, 'register')

        return is_valid
