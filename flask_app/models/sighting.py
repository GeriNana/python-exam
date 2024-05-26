from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Sighting:
    db_name = "sighting"

    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.description = data['description']
        self.date_of_sighting = data['date_of_sighting']
        self.number_of_sasquatches = data['number_of_sasquatches']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.skeptic_count = data.get('skeptic_count', 0)
        self.user = data.get('user', None)


    @classmethod
    def create(cls, data):
        query = """
        INSERT INTO sightings (location, date_of_sighting, description, number_of_sasquatches, user_id) 
        VALUES (%(location)s, %(date_of_sighting)s, %(description)s, %(number_of_sasquatches)s, %(user_id)s);
        """
        print("Running Query with Data:", data)  # Debugging line
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = """
        SELECT sightings.*, users.first_name, users.last_name, COUNT(likes.id) AS skeptic_count
        FROM sightings
        LEFT JOIN users ON sightings.user_id = users.id
        LEFT JOIN likes ON sightings.id = likes.sighting_id
        GROUP BY sightings.id;
        """
        results = connectToMySQL(cls.db_name).query_db(query)
        sightings = []
        if results:
            for row in results:
                sighting = {
                    'id': row['id'],
                    'location': row['location'],
                    'description': row['description'],
                    'date_of_sighting': row['date_of_sighting'],
                    'number_of_sasquatches': row['number_of_sasquatches'],
                    'user_id': row['user_id'],
                    'user': {
                        'first_name': row['first_name'],
                        'last_name': row['last_name']
                    },
                    'created_at': row['created_at'],
                    'updated_at': row['updated_at'],
                    'skeptic_count': row['skeptic_count']
                }
                sightings.append(sighting)
        return sightings

    @classmethod
    def get_sighting_by_id(cls, data):
        query = """
        SELECT sightings.*, users.first_name, users.last_name 
        FROM sightings 
        LEFT JOIN users ON sightings.user_id = users.id 
        WHERE sightings.id = %(id)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            row = results[0]
            sighting = {
                'id': row['id'],
                'location': row['location'],
                'description': row['description'],
                'date_of_sighting': row['date_of_sighting'],
                'number_of_sasquatches': row['number_of_sasquatches'],
                'user_id': row['user_id'],
                'user': {
                    'first_name': row['first_name'],
                    'last_name': row['last_name']
                },
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }
            return sighting
        return None

    @classmethod
    def update(cls, data):
        query = """
        UPDATE sightings 
        SET location = %(location)s, description = %(description)s, date_of_sighting = %(date_of_sighting)s, number_of_sasquatches = %(number_of_sasquatches)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_users_who_liked_by_sighting_id(cls, data):
        query = """
        SELECT users.* 
        FROM likes 
        LEFT JOIN users ON likes.user_id = users.id 
        WHERE likes.sighting_id = %(sighting_id)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        users = []
        if results:
            for row in results:
                user = {
                    'id': row['id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'created_at': row['created_at'],
                    'updated_at': row['updated_at']
                }
                users.append(user)
        return users
    

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM sightings WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)


    @classmethod
    def add_like(cls, data):
        query = "INSERT INTO likes (user_id, sighting_id) VALUES (%(user_id)s, %(sighting_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def remove_like(cls, data):
        query = "DELETE FROM likes WHERE user_id = %(user_id)s AND sighting_id = %(sighting_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_sighting(sighting):
        is_valid = True
        if len(sighting['location']) < 2:
            flash('Location should be more or equal to 2 characters', 'location')
            is_valid = False
        if len(sighting['description']) < 10:
            flash('Description should be more or equal to 10 characters', 'description')
            is_valid = False
        if len(sighting['date_of_sighting']) < 1:
            flash('Date of Sighting is required', 'date_of_sighting')
            is_valid = False
        if len(sighting['number_of_sasquatches']) < 1:
            flash('Number of Sasquatches is required', 'number_of_sasquatches')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_sighting_update(sighting):
        return Sighting.validate_sighting(sighting)
