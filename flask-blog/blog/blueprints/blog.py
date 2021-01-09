from flask import Blueprint, render_template,request ,session, redirect,url_for, flash
from blog.db import get_db
import sqlite3
import datetime
from functools import wraps
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, TextAreaField
from ..forms import PostForm, ReplyPostForm, EditPostForm

# define our blueprint
blog_bp = Blueprint('blog', __name__)

def login_required(f):
    @wraps(f)

    
    def check(*args, **kwargs):
        

        if 'username' in session:
            return f(*args, **kwargs)
            
        else:

            return redirect('/login')
            # , next=request.url )
            
    return check








@blog_bp.route('/')
@blog_bp.route('/posts')
@login_required
def index():
    # get the DB connection
    db = get_db()

    # retrieve all posts
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, firstname , lastname'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    # render 'blog' blueprint with posts
    return render_template('blog/index.html', posts = posts)


@blog_bp.route('/posts/display/<int:id>')
@login_required
def display_myposts(id):
        # get the DB connection
    db = get_db()

    # retrieve all posts
    posts = db.execute(f'''select * from post WHERE author_id = {id}''').fetchall()
    user = db.execute(f'''select * from user WHERE id = {id}''').fetchall()


    # render 'blog' blueprint with posts
    return render_template('blog/display.html', posts = posts , user=user)



@blog_bp.route('/add/post', methods = ['GET', 'POST'])
@login_required
def add_post():


    post_form = PostForm()

    if post_form.validate_on_submit():
        # read post values from the form
        title = post_form.title.data
        body = post_form.body.data 

        # read the 'uid' from the session for the current logged in user
        author_id = session['uid']

        # get the DB connection
        db = get_db()
        
        # insert post into database
        try:
            # execute the SQL insert statement
            db.execute("INSERT INTO post (author_id, title, body) VALUES (?, ?,?);", (author_id, title, body))
            
            # commit changes to the database
            db.commit()
            flash('You were successfully Add')
            return redirect('/posts') 

        except sqlite3.Error as er:
            print(f"SQLite error: { (' '.join(er.args)) }")
            return redirect("/404")

    # if the user is not logged in, redirect to '/login' 
    if "uid" not in session:
        return redirect('/login')
    
    # else, render the template
    return render_template("blog/add-post.html", form = post_form)


@blog_bp.route('/post/delete/<int:id>', methods = ['GET', 'POST'])
@login_required
def delete_post(id):

    # get the DB connection
    db = get_db()

    
    # post_id = db.execute(f"SELECT id FROM post WHERE id = {id} ")
    # print(type(post_id))
    db.execute(f"DELETE FROM post WHERE id = {id} ")
    
    db.commit()


    return redirect('/profile')



@blog_bp.route('/post/edit/<int:id>', methods = ['GET', 'POST'])
@login_required
def edit_post(id):

    edit_post_form = EditPostForm() # 

    
    if edit_post_form.validate_on_submit():
        # read post values from the form
        new_title = edit_post_form.new_title.data
        new_body = edit_post_form.new_body.data 


        # get the DB connection
        db = get_db()
        
        
        try:
            
            db.execute(f"UPDATE post SET title = '{new_title}', body = '{new_body}' WHERE id = '{id}' ")    
            
            # commit changes to the database
            db.commit()
            
            return redirect('/posts') 

        except sqlite3.Error as er:
            print(f"SQLite error: { (' '.join(er.args)) }")
            return redirect("/404")

    # if the user is not logged in, redirect to '/login' 
    if "uid" not in session:
        return redirect('/login')
    
    # else, render the template
    return render_template("blog/edit_post.html", form = edit_post_form)


@blog_bp.route('/post/reply/<int:id>', methods = ['GET', 'POST'])
@login_required
def reply_post(id):
    db = get_db()
    reply_form = ReplyPostForm()

    if reply_form.validate_on_submit():
        # read post values from the form
        body = reply_form.body.data 
        author_id = session['uid']

        
        try:
            # execute the SQL insert statement
            db.execute("INSERT INTO reply (post_id,author_id,body) VALUES (?,?,?);", (id,author_id,body,))
            
            # commit changes to the database
            db.commit()
            return redirect(url_for('blog.reply_post', id = id))

        except sqlite3.Error as er:
            print(f"SQLite error: { (' '.join(er.args)) }")
            return redirect("/404")

        
    # Display the reply section
    
    # retrieve post
    mypost = db.execute(f'''select * from post WHERE id = {id}''').fetchone()
    
    # retrieve first and last name from author post
    author_id = mypost['author_id']
    post_author = db.execute(f'''select * from user WHERE id = {author_id}''').fetchone()
    

    #retrieve replies 
    replies = db.execute(f'''select * from reply WHERE post_id = {id}''').fetchall()

    
    users = db.execute("select * from user").fetchall()



    #render the template
    return render_template("blog/reply_post.html", mypost = mypost, post_author = post_author, form = reply_form, replies = replies, users = users)
