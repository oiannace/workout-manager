from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from flask_jwt_extended import (jwt_required, get_jwt_identity)

from werkzeug.exceptions import abort

from workout_manager.db import get_db

import json
import datetime
bp = Blueprint('workout', __name__, url_prefix='/workout')

@bp.route('/add', methods=('POST',))
@jwt_required()
def add():
    if request.method == 'POST':
        today = datetime.datetime.now()
        workout_json = request.json
        error = None
        
        db = get_db()
        user_id = db.execute(
            'SELECT id FROM user WHERE username = ?', (get_jwt_identity(),)
        ).fetchone()
        user_id = tuple(user_id)[0]
        exercise_id = db.execute(
            'SELECT id FROM exercise_stats WHERE exercise_name = ?', (workout_json.get('exercise_name'),)
        ).fetchone()
        exercise_id = tuple(exercise_id)[0]
        print(user_id, exercise_id)
        if not workout_json.get('exercise_name'):
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            
            db.execute(
                'INSERT INTO workout (exercise_id, user_id, year, month, day )'
                ' VALUES (?, ?, ?, ?, ?)',
                (exercise_id, user_id, today.year, today.month, today.day )
                )
            db.commit()
            

    return json.dumps(exercise_id)

@bp.route('/get', methods=('GET',))
def get():
    
    db = get_db()
    workout_date = request.args.get('date')
    workout_day = workout_date[0:2]
    workout_month = workout_date[3:5]
    workout_year = workout_date[6:10]
    print(workout_date)
    workout = db.execute(
        'SELECT id, exercise_id, user_id FROM workout WHERE year = ? and month = ? and day = ?', (workout_year, workout_month, workout_day)
    ).fetchall()
    workout_tuple = [tuple(row) for row in workout]
    
    return json.dumps(workout_tuple)










