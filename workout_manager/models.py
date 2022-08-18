import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token
from flask import jsonify

class Schema:
    def __init__(self):
        self.conn = sqlite3.connect('workout_manager.db')
        self.create_user_table()
        self.create_exercise_table()
        

    def __del__(self):
        # body of destructor
        self.conn.commit()
        

    def create_exercise_table(self):

        query = """
        CREATE TABLE IF NOT EXISTS "exercise" (
          id INTEGER PRIMARY KEY,
          exercise_name TEXT NOT NULL,
          num_sets INTEGER,
          num_reps INTEGER,
          weight INTEGER,
          UserId INTEGER FOREIGNKEY REFERENCES User(id)
        );
        """

        self.conn.execute(query)

    def create_user_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "User" (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
        );
        """
        self.conn.execute(query)


class exerciseModel:
    TABLENAME = "exercise"

    def __init__(self):
        self.conn = sqlite3.connect('workout_manager.db')
        self.conn.row_factory = sqlite3.Row

    def __del__(self):
        # body of destructor
        self.conn.commit()

    def get_by_id(self, _id):
        where_clause = f"AND id={_id}"
        return self.list_items(where_clause)

    def create(self, params):
        print (params)
        query = f'insert into {self.TABLENAME} ' \
                f'(exercise_name, num_sets, num_reps, weight, UserId) ' \
                f'values ("{params.get("exercise_name")}","{params.get("num_sets")}",' \
                f'"{params.get("num_reps")}","{params.get("weight")}", "{params.get("UserId")}")'

        
        result = self.conn.execute(query)
        self.conn.commit()
        return self.get_by_id(result.lastrowid)

    def delete(self, item_id):
        query = f"UPDATE {self.TABLENAME} " \
                f"SET _is_deleted =  {1} " \
                f"WHERE id = {item_id}"
        print (query)
        self.conn.execute(query)
        self.conn.commit()
        return self.list_items()

    def update(self, item_id, update_dict):
        """
        column: value
        Title: new title
        """
        set_query = ", ".join([f'{column} = "{value}"'
                     for column, value in update_dict.items()])

        query = f"UPDATE {self.TABLENAME} " \
                f"SET {set_query} " \
                f"WHERE id = {item_id}"
    
        self.conn.execute(query)
        self.conn.commit()
        return self.get_by_id(item_id)

    def list_items(self, where_clause=""):
        query = f"SELECT id, exercise_name, num_sets, num_reps, weight, UserId " \
                f"from {self.TABLENAME}" 
                # WHERE _is_deleted != {1} " + where_clause
        print (query)
        result_set = self.conn.execute(query).fetchall()
        print (result_set)
        result = [{column: row[i]
                  for i, column in enumerate(result_set[0].keys())}
                  for row in result_set]
        return result


class userModel:
    TABLENAME = "User"

    def __init__(self):
        self.conn = sqlite3.connect('workout_manager.db')
        self.conn.row_factory = sqlite3.Row

    def __del__(self):
        # body of destructor
        self.conn.commit()
        

    def register(self, params):
        query = f"insert into {self.TABLENAME} (username, password) values ('{params.get('username')}', '{generate_password_hash(params.get('password'))}')"
        result = self.conn.execute(query)
        self.conn.commit()
        return result

    def login(self, params):
        query = f'SELECT * from {self.TABLENAME} where username = "{params.get("username")}"' 
        user = self.conn.execute(query).fetchone()
        error = None

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], params.get("password")):
            error = 'Incorrect password.'

        if error == None:
            access_token = create_access_token(identity=params.get("username"))
            return jsonify(access_token=access_token)

        return error




