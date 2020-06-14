from flask import Blueprint, render_template, request, g

from . import db
from .auth import login_required
import psycopg2
import psycopg2.extras


bp = Blueprint("todos", __name__)

def display_todos():

    user = get_user_info()
    if user['id'] != g.user['id']:
        abort(403)

    # Displays all the to-dos on the todo.html
    cur = db.get_db().cursor()
    cur.execute('SELECT * FROM todos WHERE user_id = %s', (g.user['id'], ))
    todos = cur.fetchall()
    cur.close()
    return todos

def get_user_info():
    # Gets users name to be more personalized
    cur = db.get_db().cursor()
    cur.execute('SELECT * FROM users WHERE id = %s', (g.user['id'], ))
    user = cur.fetchone()
    return user

@bp.route("/home", methods=('GET', 'POST'))
@login_required
def todo():
    """View for home page which shows list of to-do items."""
    user = get_user_info()
    if user['id'] != g.user['id']:
        abort(403)

    if request.method == 'POST':
        # the variable filter feature is equal to the form dropDown
        filterFeature = request.form['dropDown']
        # get the database connection
        with db.get_db() as con:
            # Begin the transaction
            with con.cursor() as cur:

                # code only runs if the request is toDo
                if filterFeature == 'toDo':
                    # only displays todos with a completed field of false
                    cur.execute(
                        'SELECT * FROM todos WHERE completed = False AND user_id = %s', (g.user['id'], ))
                    todos = cur.fetchall()
                    cur.close()
                # code only runs if the request is finished
                if filterFeature == 'finished':
                    # only displays todos with a completed field of true
                    cur.execute(
                        'SELECT * FROM todos WHERE completed = True AND user_id = %s', (g.user['id'], ))
                    todos = cur.fetchall()
                    cur.close()
                # code only runs if the request is addTasks
                if filterFeature == 'allTasks':
                    # Displays all the to-dos on the todo.html
                    todos = display_todos()

                return render_template("todo.html", todos=todos)

    todos = display_todos()

    return render_template("todo.html", todos=todos, user=user)

@bp.route('/addATask', methods=('GET', 'POST'))
@login_required
def adding_A_Task():
    """Adding a task function so the user can update their to-dos"""

    user = get_user_info()
    if user['id'] != g.user['id']:
        abort(403)

    if request.method == 'POST':
        # the variable addTask is equal to the form data on addTask
        addTask = request.form['addTask']

        # get the database connection
        with db.get_db() as con:
            # Begin the transaction
            with con.cursor() as cur:

                # Inserts the description the user filled into the form using SQL
                cur.execute("""INSERT INTO todos (description, completed, user_id, created_at)
                VALUES (%s, %s, %s, NOW())
                """,
                            (addTask, False, g.user['id'], )
                            )
                con.commit()

    todos = display_todos()

    return render_template("todo.html", todos=todos, user=user)

@bp.route('/Done', methods=('GET', 'POST'))
@login_required
def task_is_done():
    """Marking a Task as completed so the user knows they are done"""

    user = get_user_info()
    if user['id'] != g.user['id']:
        abort(403)


    if request.method == 'POST':

        doneTask = request.form["doneButton"]

        # get the database connection
        with db.get_db() as con:
            # Begin the transaction
            with con.cursor() as cur:

                cur.execute(""" UPDATE todos
                            SET completed = True
                            WHERE id = %s
                            AND user_id = %s""",
                            (doneTask, g.user['id'])
                            )
                con.commit()

    todos = display_todos()

    return render_template("todo.html", todos=todos, user=user)

@bp.route('/Edit', methods=('GET', 'POST'))
@login_required
def editing_feature():
    """So the user can change the description of a To Do item"""
    user = get_user_info()
    if user['id'] != g.user['id']:
        abort(403)

    if request.method == 'POST':

        EditDesc = request.form['EditDesc']
        EditId = request.form['EditButton']
        # get the database connection
        with db.get_db() as con:
            # Begin the transaction
            with con.cursor() as cur:

                # Changes the description the user filled into the form using SQL
                cur.execute(""" UPDATE todos
                            SET description = %s
                            WHERE id = %s
                            """,
                            (EditDesc, EditId, ))
                con.commit()

    todos = display_todos()

    return render_template("todo.html", todos=todos, user=user)

@bp.route('/RedoTask', methods=('GET', 'POST'))
@login_required
def redo_a_task():
    """Allows the user to unfinish a task
    so they can complete it again"""
    user = get_user_info()
    if user['id'] != g.user['id']:
        abort(403)

    if request.method == 'POST':

        redo = request.form['redoTask']
        # get the database connection
        with db.get_db() as con:
            # Begin the transaction
            with con.cursor() as cur:

                #Updates the table so the task is now "uncompleted"
                cur.execute("""UPDATE todos
                            SET completed = False
                            WHERE id = %s
                            """,
                            (redo, )
                            )
                con.commit()

    # Displays all the to-dos on the todo.html
    todos = display_todos()

    return render_template("todo.html", todos=todos, user=user)

@bp.route('/Delete', methods=('GET', 'POST'))
@login_required
def delete_feature():
    """So the user can delete a post that takes up space"""
    user = get_user_info()
    if user['id'] != g.user['id']:
        abort(403)

    if request.method == 'POST':

        deleteTask = request.form['deleteButton']
        # get the database connection
        with db.get_db() as con:
            # Begin the transaction
            with con.cursor() as cur:

                # Changes the table so the task is removed from the table
                cur.execute(""" DELETE FROM todos WHERE id = %s
                """,
                            (deleteTask, g.user['id'])
                            )
                con.commit()

    todos = display_todos()

    return render_template("todo.html", todos=todos, user=user)
