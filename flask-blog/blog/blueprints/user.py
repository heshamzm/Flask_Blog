from flask import Blueprint, render_template,request ,redirect, session
from blog.db import get_db
import sqlite3
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, PasswordField, TextAreaField

# define our blueprint
user_bp = Blueprint('user', __name__)


class User(FlaskForm):
    username = StringField("Username : ", [validators.InputRequired()])
    password = PasswordField("Password : ", [validators.InputRequired()])
    submit = SubmitField("Add User")
    edit = SubmitField("Edit User")

    first_name = StringField("First name : ", [validators.InputRequired()])
    last_name = StringField("Last name : ", [validators.InputRequired()])
    biography = TextAreaField("Biography : ")


@user_bp.route('/session')
def show_session():
    return dict(session)

@user_bp.route('/add/user', methods=['GET', 'POST'])
def add_user():

    user = User()

    if user.validate_on_submit():
    
        username = user.username.data
        password = user.password.data
        first_name = user.first_name.data
        last_name = user.last_name.data
        biography = user.biography.data
        # get the DB connection
        db = get_db()

        # insert user into DB
        try:
            # execute our insert SQL statement
            db.execute("INSERT INTO user (username, password , firstname , lastname , biography ) VALUES (?, ? , ? , ?, ?);", (username, password, first_name,last_name, biography))

            # write changes to DB
            db.commit()
            
            return redirect("/users")

        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return redirect("/404")

    return render_template('user/index.html' , form = user )

@user_bp.route('/profile' , methods=['GET', 'POST'])
def profile():

    # profile = User()

    # username = profile.username.data

    current_user = session['uid']

    db = get_db()

    # user= db.execute('SELECT * FROM user WHERE username LIKE ?',(username,)).fetchone()

    user = db.execute(" SELECT * FROM user WHERE id = '1' ").fetchone()

    return render_template("user/profile.html", user = user) 


@user_bp.route('/edit/user', methods=['GET', 'POST'])
def edit_user():

    edit_form = User()

    if edit_form.validate_on_submit():
        new_firstname = edit_form.first_name.data
        new_lasttname = edit_form.last_name.data
        new_bio = edit_form.biography.data

        db = get_db()

        try:
            
            db.execute("""UPDATE user
SET firstname = 'new_firstname', lastname = 'new_lasttname', biography = 'new_bio',
WHERE id = 'session[uid]';""")
            
            db.commit()


            return redirect('/profile') 

        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return redirect("/404")

    return render_template("user/edituser.html", form = edit_form)
    

@user_bp.route('/users')
def get_users():
    # get the DB connection
    db = get_db()

    # get all users from the db
    users = db.execute('select * from user').fetchall()

    # render 'list.html' blueprint with users
    return render_template('user/list.html', users=users)
