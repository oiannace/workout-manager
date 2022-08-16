import functools

from flask import (
    Blueprint, current_app, flash, jsonify, request, g, redirect, render_template, request, session, url_for
)
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash

from workout_manager.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            #else:
                #return redirect(url_for("auth.login"))
        flash(error)

    return jsonify({"msg":"You registered"})

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token)

        flash(error)

    return "eng of login"

