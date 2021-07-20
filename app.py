""" Flask app for Notes """

from flask import Flask, redirect, session, flash
from flask.templating import render_template
from forms import LoginForm, RegisterForm, NoteAddOrEditForm
from werkzeug.exceptions import Unauthorized


from models import db, connect_db, User, Note

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

USERNAME_KEY = 'username'


@app.route("/")
def redirect_register():
    """ Redirects user to the register user page. """

    return redirect("/register")


################################################################################
# User routes


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

        session[USERNAME_KEY] = new_user.username

        return redirect(f"/users/{new_user.username}")
    
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
            session[USERNAME_KEY] = user.username
            
            return redirect(f"/users/{username}")
        else:
            form.username.errors = ["Bad username/password"]

    return render_template("login.html", form=form)



@app.route("/users/<username>")
def user_info_display(username):
    """ Displays user information if login. """

    if username == session[USERNAME_KEY]:
        user = User.query.get_or_404(username)
        return render_template("user_detail.html", user=user, notes=user.notes)   

    else:
        flash("You do not have access to this user's information.")
        return redirect(f"/users/{session[USERNAME_KEY]}")



@app.route("/logout", methods=["POST"])
def user_logout():
    """ Logout current user from website and redirect to homepage. """
    
    session.pop(USERNAME_KEY, None)   

    return redirect("/")


@app.route("/users/<username>/delete", methods=["POST"])
def user_delete(username): 
    """ Deletes current user and all associated notes. """

    user = User.query.get(username)
    notes = user.notes

    if session.get(USERNAME_KEY) != username:
        raise Unauthorized() 

    for note in notes:
        db.session.delete(note)

    db.session.delete(user)
    db.session.commit()

    return redirect("/")


################################################################################
# Note routes


@app.route("/users/<username>/notes/add", methods=["GET", "POST"])
def note_add(username):
    """ Displays and processes form to add note. """

    form = NoteAddOrEditForm()
    user = User.query.get_or_404(username)

    # raises unauthorized error if current user is unauthorized or not logged in
    if session.get(USERNAME_KEY) != username:
        raise Unauthorized() 


    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_note = Note(
                    title=title,
                    content=content, 
                    owner=username)

        db.session.add(new_note)
        db.session.commit()

        return redirect(f"/users/{username}")
    
    else: 
        return render_template("add_note.html", user=user, form=form)


@app.route("/notes/<int:note_id>/update", methods=["GET", "POST"])
def note_update(note_id):
    """ Displays and processes form to edit a note. """

    note = Note.query.get_or_404(note_id)
    form = NoteAddOrEditForm(obj=note)

    if session.get(USERNAME_KEY) != note.user.username:
        raise Unauthorized() 

    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{note.owner}")
    
    else: 
        return render_template("edit_note.html", form=form)



@app.route("/notes/<int:note_id>/delete", methods=["POST"])
def note_delete(note_id):
    """ Deletes a note. """

    note = Note.query.get(note_id)

    if session.get(USERNAME_KEY) != note.user.username:
        raise Unauthorized() 

    db.session.delete(note)
    db.session.commit()

    return redirect(f"/users/{session[USERNAME_KEY]}")

