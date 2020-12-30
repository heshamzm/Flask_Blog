from flask import Blueprint, render_template,request ,session, redirect
from blog.db import get_db
import sqlite3
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, TextAreaField

# define our blueprint
blog_bp = Blueprint('blog', __name__)


class PostForm(FlaskForm):
    title = StringField("Post Title: ", [validators.InputRequired()])
    body = TextAreaField("Post Body: ", [validators.InputRequired()])
    submit = SubmitField("Create Post")


@blog_bp.route('/')
@blog_bp.route('/posts')
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

@blog_bp.route('/add/post', methods = ['GET', 'POST'])
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
            
            return redirect('/posts') 

        except sqlite3.Error as er:
            print(f"SQLite error: { (' '.join(er.args)) }")
            return redirect("/404")

    # if the user is not logged in, redirect to '/login' 
    if "uid" not in session:
        return redirect('/login')
    
    # else, render the template
    return render_template("blog/add-post.html", form = post_form)