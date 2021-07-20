from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField 
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired


class RegisterForm(FlaskForm):
    """ Form to register new user. """

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired()])
    first_name = StringField("First name", validators=[InputRequired()])
    last_name = StringField("Last name", validators=[InputRequired()])


class LoginForm(FlaskForm):
    """ Form to login existing users"""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class NoteForm(FlaskForm):
    """ Form to add note"""

    title = StringField("Title", validators=[InputRequired()])
    content = TextAreaField("Content", validators=[InputRequired()])