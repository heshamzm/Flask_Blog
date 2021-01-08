from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators,PasswordField, TextAreaField



class PostForm(FlaskForm):
    title = StringField("Post Title: ", [validators.InputRequired()])
    body = TextAreaField("Post Body: ", [validators.InputRequired()])
    submit = SubmitField("Create Post")



class ReplyPostForm(FlaskForm):
    body = TextAreaField("Reply Body: ", [validators.InputRequired()])
    reply = SubmitField("Reply")



class EditPostForm(FlaskForm):
    new_title = StringField("Post Title: ", [validators.InputRequired()])
    new_body = TextAreaField("Post Body: ", [validators.InputRequired()])
    submit = SubmitField("Edit")

class LoginForm(FlaskForm):
    username = StringField("Username : ", [validators.InputRequired()])
    password = PasswordField("Password : ", [validators.InputRequired()])
    submit = SubmitField("Log In")

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