import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token
from flask import jsonify
import os
class Schema:
    def __init__(self):
        self.conn = psycopg2.connect(host=os.environ['flask_app_db_host'],
                                    dbname=os.environ['flask_app_db_name'],
                                    user=os.environ['flask_app_db_username'],
                                    port=5432,
                                    password=os.environ['flask_app_db_password'])
        self.cur = self.conn.cursor()
        
        #self.cur.execute("DROP TABLE IF EXISTS User, exercise;")
        self.create_user_table()
        self.create_exercise_table()
        

    def __del__(self):
        # body of destructor
        self.conn.commit()
        

    def create_exercise_table(self):

        query = """
        CREATE TABLE if not exists exercise (
          id SERIAL PRIMARY KEY,
          exercise_name TEXT NOT NULL,
          num_sets INTEGER,
          num_reps INTEGER,
          weight INTEGER,
          UserId INTEGER references app_user(id));
        """

        self.cur.execute(query)

    def create_user_table(self):
        query = """
        CREATE TABLE if not exists app_user (
        id SERIAL PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL
        );
        """
        self.cur.execute(query)



class exerciseModel:
    TABLENAME = "exercise"
    ##change these queries to the format in the register/login functions
    def __init__(self):
        self.conn = psycopg2.connect(host=os.environ['flask_app_db_host'],
                                    dbname=os.environ['flask_app_db_name'],
                                    user=os.environ['flask_app_db_username'],
                                    port=5432,
                                    password=os.environ['flask_app_db_password'])
        self.cur = self.conn.cursor()
        

    def __del__(self):
        # body of destructor
        self.conn.commit()

    def get_by_id(self, _id):
        self.cur.execute("select * from exercise where id = %s", (_id,))
        exercise = self.cur.fetchall()
        return exercise

    def get_by_name(self, name):
        self.cur.execute("select * from exercise where exercise_name = %s", (name,))
        exercise = self.cur.fetchall()
        return exercise

    def create(self, params):
        query = sql.SQL("insert into exercise (exercise_name, num_sets, num_reps, weight, UserId) values (%s, %s, %s, %s, %s)")
        self.cur.execute(query, (params.get("exercise_name"), params.get("num_sets"), params.get("num_reps"), params.get("weight"), params.get("UserId")))
        self.conn.commit()
        return self.get_by_name(params.get("exercise_name"))

    def delete_by_id(self, item_id):
        query = sql.SQL("DELETE FROM exercise where id = %s")
        self.cur.execute(query, (item_id,))
        self.conn.commit()
        return self.list_exercises()

    def update(self, exercise_id, update_dict):
        """
        column: value
        Title: new title
        """
        set_query = ", ".join([(f'{column} = "{value}"') if type(value) == str else (f'{column} = {value}') for column, value in update_dict.items()])

        query = sql.SQL("UPDATE exercise set %s where id = %s")
        self.cur.execute(query, (AsIs(set_query), exercise_id))
        self.conn.commit()
        return self.get_by_id(exercise_id)

    def list_exercises(self):
        self.cur.execute("select * from exercise")
        exercises = self.cur.fetchall()
        return exercises


class userModel:
    TABLENAME = "app_user"

    def __init__(self):
        self.conn = psycopg2.connect(host=os.environ['flask_app_db_host'],
                                    dbname=os.environ['flask_app_db_name'],
                                    user=os.environ['flask_app_db_username'],
                                    port=5432,
                                    password=os.environ['flask_app_db_password'])
        self.cur = self.conn.cursor()
        

    def __del__(self):
        # body of destructor
        self.conn.commit()
        

    def register(self, params):
        query = sql.SQL("insert into app_user (username, password) values (%s, %s)")
        self.cur.execute(query, (params.get("username"), generate_password_hash(params.get("password"))))
        
        self.conn.commit()
        return "User successfully registered"

    def login(self, params):
        #need to fetchall on self.cur not on self.cur.execute
        self.cur.execute("select * from app_user where username = %s", (params.get("username"),))
        user = self.cur.fetchall()
        
        error = None

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[0][2], params.get("password")):
            error = 'Incorrect password.'

        if error == None:
            access_token = create_access_token(identity=params.get("username"))
            return jsonify(access_token=access_token)

        return error




