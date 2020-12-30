from flask import Blueprint, render_template,request ,redirect,session
from blog.db import get_db
import sqlite3
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, PasswordField

# define our blueprint
login_bp = Blueprint('login', __name__)

class LoginForm(FlaskForm):
    username = StringField("Username : ", [validators.InputRequired()])
    password = PasswordField("Password : ", [validators.InputRequired()])
    submit = SubmitField("Log In")

@login_bp.route('/login', methods =['POST','GET'])
def login():
    login = LoginForm()
    if login.validate_on_submit():
        # read values from the login wtform
        username = login.username.data
        password = login.password.data
        
        # get the DB connection
        db = get_db()
        
        # insert user into db
        try:
            # get user by username
            user= db.execute('SELECT * FROM user WHERE username LIKE ?',(username,)).fetchone()
            # check if username exists
            if user  != None:
                # check if credentials are valid
                if user['username'] == username and user['password'] == password:
                    # store the user ID in the session  
                    session['uid']= user['id']  
                    session['username'] = user['username']
            return redirect("/posts")

        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return redirect("/404") 
        # render the login template
    return render_template('login/login.html', form = login)
    
        

@login_bp.route('/session')
def show_session():
    return dict(session)

@login_bp.route('/logout')
def logout():
    # pop 'uid' from session
    session.clear()

    # redirect to index
    return redirect("/")