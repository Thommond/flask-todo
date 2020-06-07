from flask import Blueprint, render_template, request, url_for, session, g, redirect, flash

import functools

from werkzeug.security import check_password_hash, generate_password_hash

from . import db
import psycopg2
import psycopg2.extras

bp = Blueprint("auth", __name__)


@bp.route("/register", methods=('GET', 'POST'))
def register():
    """"So a new user can sign up for the to do app"""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']
        error = None

        # get the database connection
        with db.get_db() as con:
            # Begin the transaction
            with con.cursor() as cur:

                # Checking if field were filled out if not error
                if not email:
                    error = 'Username is required.'
                elif not password:
                    error = 'Password is required.'
                    # Checking if user does not already exist
                query = 'SELECT user_id FROM users WHERE email = %s'
                cur.execute(query, (email,))
                check = cur.fetchone()
                if check is not None:
                    error = 'Email is already taken.'.format(email)

                    # Enterning forms if no errors
                if error is None:
                    cur.execute(
                    'INSERT INTO users (email, password) VALUES (%s, %s)',
                    (email, generate_password_hash(password), )
                    )
                    con.commit()
                    
                    return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route("/login", methods=('GET', 'POST'))
def login():
    """So users can log in and remember their data"""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']
        error = None
        # get the database connection
        with db.get_db() as con:
            # Begin the transaction
            with con.cursor() as cur:

                query = 'SELECT * FROM users WHERE email = %s'
                cur.execute(query, (email,))
                user = cur.fetchone()
                print(user)
                if user is None:
                    error = 'Incorrect username or password'

                if not check_password_hash(password, user['password']):
                    error = 'Incorrect username or password'

                if error is None:
                    session.clear()
                    session['user_id'] = user['id']
                    return redirect(url_for('todo'))

            flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    """Gets the g.user of a login user and grabs session"""
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = db.get_db().execute(
            'SELECT * FROM users WHERE user_id = %s', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    """Ends user session"""
    session.clear()
    return redirect(url_for('index'))

#Enables for decorator on routes
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
