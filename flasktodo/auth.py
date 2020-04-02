from flask import Blueprint, render_template, redirect, url_for, request
from . import db

bp = Blueprint("auth", __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        con = db.get_db()
        error = None

        if not username:
            error = 'Username is required.'
        if not password:
            error = 'Password is required.'
        if con.cursor().execute(
            'SELECT id FROM users WHERE username = %s', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            con.cursor().execute(
                'INSERT INTO users (username, password) VALUES (%s, %s)',
                (username, password)
            )
            con.commit()
            return redirect(url_for('auth.login'))

        flash(error)
        print(error)

    return render_template('auth/register.html')
