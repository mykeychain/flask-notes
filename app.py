""" Flask app for Notes """

from flask import Flask, redirect, session, request, flash
from flask.templating import render_template
from wtforms.fields.simple import PasswordField
from forms import LoginForm, RegisterForm

from models import db, connect_db, User, Note

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"


@app.route("/")
def redirect_register():
    """ Redirects user to the register user page. """

    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register_show_form_and_process():
    """ Displays form to register new user. """

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        db.session.commit()

        session["username"] = new_user.username

        return redirect("/secret")
    
    else: 
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_show_form_and_process():
    """ Displays and processes login form. """

    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        
        if user:
            session["username"] = user.username
            
            return redirect(f"/users/{username}")
        else:
            form.username.errors = ["Bad username/password"]

    return render_template("login.html", form=form)


@app.route("/users/<username>")
def user_info_display(username):
    """ Displays user information if login. """

    if username == session["username"]:
        user = User.query.get_or_404(username)
        return render_template("user_detail.html", user=user, notes=user.notes)   

    else:
        flash("You have no access to our secret, please login first")
        return redirect("/register")
        

@app.route("/logout", methods=["POST"])
def logout_user():
    """ Logout current user from website and redirect to homepage"""
    
    session.pop("username", None)   

    return redirect("/")





