from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from flask_jwt_extended import (jwt_required, get_jwt_identity)

from werkzeug.exceptions import abort

from workout_manager.db import get_db

import json

bp = Blueprint('exercise', __name__, url_prefix='/exercise')

@bp.route('/add', methods=('POST',))
@jwt_required()
def add():
    if request.method == 'POST':
        exercise_json = request.json
        error = None
        print(exercise_json, get_jwt_identity())
        
        db = get_db()
        user_id = db.execute(
            'SELECT id FROM user WHERE username = ?', (get_jwt_identity(),)
        ).fetchone()
        user_id = tuple(user_id)[0]
        print(user_id)
        
        if not exercise_json.get('exercise_name'):
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO exercise_stats (user_id, exercise_name, num_sets, num_reps, weight)'
                ' VALUES (?, ?, ?, ?, ?)',
                (user_id, exercise_json.get('exercise_name'), exercise_json.get('num_sets'), exercise_json.get('num_reps'), exercise_json.get('weight'))
            )
            db.commit()
            #return redirect(url_for('blog.index'))

    return "end of add"

@bp.route('/get-stats', methods=('GET',))
def get_stats():
    
    db = get_db()
    exercise_name = request.args.get('exercise_name')
    
    exercise_stats = db.execute(
        'SELECT exercise_name, num_sets, num_reps, weight FROM exercise_stats WHERE exercise_name = ?', (exercise_name,)
    ).fetchall()
    exercise_stats_tuple = [tuple(row) for row in exercise_stats]
    
    return json.dumps(exercise_stats_tuple)
    