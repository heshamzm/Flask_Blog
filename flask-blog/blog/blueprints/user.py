from flask import Blueprint, render_template,request ,redirect, session , flash
from blog.db import get_db
import sqlite3
from functools import wraps
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, PasswordField, TextAreaField 


# define our blueprint
user_bp = Blueprint('user', __name__)

def login_required(f):
    @wraps(f)

    
    def check(*args, **kwargs):
        

        if 'username' in session:
            return f(*args, **kwargs)
            
        else:

            return redirect('/login')
            # , next=request.url )
            
    return check


class User(FlaskForm):
    username = StringField("Username : ", [validators.InputRequired()])
    password = PasswordField("Password : ", [validators.InputRequired()])
    submit = SubmitField("Add User")
    first_name = StringField("First name : ", [validators.InputRequired()])
    last_name = StringField("Last name : ", [validators.InputRequired()])
    biography = TextAreaField("Biography : ")


class Edit(FlaskForm):
    first_name = StringField("First name : ", [validators.InputRequired()])
    last_name = StringField("Last name : ", [validators.InputRequired()])
    biography = TextAreaField("Biography : ")
    edit = SubmitField("Edit User")


class Change_Password(FlaskForm):
    old_password = PasswordField("Old Password : ", [validators.InputRequired()])
    password = PasswordField('New Password', [validators.InputRequired(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField("Confirm Password : ", [validators.InputRequired()])
    submit = SubmitField("Change Password")



@user_bp.route('/change_password' , methods=['POST' , 'GET'])
@login_required
def change_password():
    change_form = Change_Password()
    
    if change_form.validate_on_submit():
        oldpassword = change_form.old_password.data
        newpassword = change_form.password.data
    

        current_user = session['uid']
        db = get_db()
        user = db.execute('SELECT * FROM user WHERE id LIKE ?',(current_user,)).fetchone()

        if oldpassword ==  user['password']:
            if oldpassword != newpassword:
            
                try:

                    db.execute(f"UPDATE user SET password = '{newpassword}' WHERE id = '{current_user}' ")
                        
                        
                    db.commit()
                    
                    return redirect("/users")

                except sqlite3.Error as er:
                    print('SQLite error: %s' % (' '.join(er.args)))
                    return redirect("/404")
            
            else :
                pass
        

        else:
            pass


    return render_template('user/change_password.html' , form = change_form )


@user_bp.route('/session')
def show_session():
    return dict(session)

@user_bp.route('/add/user', methods=['GET', 'POST'])
@login_required
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
@login_required
def profile():

    current_user = session['uid']

    db = get_db()

    user = db.execute('SELECT * FROM user WHERE id LIKE ?',(current_user,)).fetchone()
    posts = db.execute('SELECT * FROM post WHERE author_id LIKE ? ORDER BY created DESC',(current_user,)).fetchmany(3)

    
    # for i in range(len(posts)):        
    #     i = i + 1  
        
    flash('You were successfully logged in')

    return render_template("user/profile.html", user = user, posts = posts ) 


@user_bp.route('/edit/user', methods=['GET', 'POST'])
@login_required
def edit_user():

    current_user = session['uid']

    edit_form = Edit() # 

    #set values in the form
    edit_form.first_name.data=session['firstname']
    edit_form.last_name.data=session['lastname']
    edit_form.biography.data=session['biography']
    print(edit_form.first_name)

    

    if edit_form.validate_on_submit():
        new_firstname = edit_form.first_name.data
        new_lasttname = edit_form.last_name.data
        new_bio = edit_form.biography.data

        print(new_firstname)

        db = get_db()

        try:
            
            db.execute(f"""UPDATE user
SET firstname = '{new_firstname}', lastname = '{new_lasttname}', biography = '{new_bio}'
WHERE id = '{current_user}' """)
            
            db.commit()


            return redirect('/profile') 

        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return redirect("/404")

    return render_template("user/edituser.html", form = edit_form)
    

@user_bp.route('/users')
@login_required
def get_users():
    # get the DB connection
    db = get_db()

    # get all users from the db
    users = db.execute('select * from user').fetchall()

    # render 'list.html' blueprint with users
    return render_template('user/list.html', users=users)
