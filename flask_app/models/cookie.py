from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Cookie:
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.cookie_type = data.get('cookie_type')
        self.box_nums = data.get('box_nums')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
    
    @staticmethod
    def validate_order(order):
        is_valid = True
        if len(order.get('name')) < 2:
            flash('Name must include at least two characters', 'name')
            is_valid = False
        if len(order.get('cookie_type')) < 2:
            flash('Cookie type must include at least two characters', 'cookie_type')
            is_valid = False
        if int(order.get('box_nums')) < 1:
            flash('Must order at least one box of cookies', 'box_nums')
            is_valid = False
        return is_valid

    @classmethod
    def get_all_cookies(cls):
        query = """SELECT * 
        FROM cookies 
        ORDER BY cookie_type ASC;
        """
        results = connectToMySQL("cookies_schema").query_db(query)
        cookie_objects = []
        for row in results:
            cookie_objects.append(cls(row))
        return cookie_objects
    
    @classmethod
    def add_cookie(cls, data):
        query = """INSERT INTO cookies (name, cookie_type, box_nums)
        VALUES (%(name)s, %(cookie_type)s, %(box_nums)s);
        """
        return connectToMySQL("cookies_schema").query_db(query, data)

    @classmethod
    def get_one (cls, data):
        query = """SELECT *
        FROM cookies
        WHERE id = %(id)s;
        """
        result = connectToMySQL("cookies_schema").query_db(query, data)
        cookie_object = cls(result[0])
        return cookie_object
    
    @classmethod
    def udpate_order (cls, data):
        query = """UPDATE cookies
        SET name = %(name)s, cookie_type = %(cookie_type)s, box_nums = %(box_nums)s
        WHERE id = %(id)s;
        """
        return connectToMySQL("cookies_schema").query_db(query, data)
    
    @classmethod
    def destroy_order (cls, data):
        query = """DELETE FROM cookies
        WHERE id = %(id)s;
        """
        return connectToMySQL("cookies_schema").query_db(query, data)