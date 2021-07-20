from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired

class RegisterForm(FlaskForm):
    """ Form to register new user. """

    username = StringField("Username", validators=[InputRequired()])

    password = PasswordField("Password", validators=[InputRequired()])

    email = EmailField("Email", validators=[InputRequired()])

    first_name = StringField("First name", validators=[InputRequired()])

    last_name = StringField("Last name", validators=[InputRequired()])


