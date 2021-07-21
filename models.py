""" Models for Notes """

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """ Connects database """

    db.app = app
    db.init_app(app)


class User(db.Model):
    """ User. """

    __tablename__ = "users"

    username = db.Column(
        db.String(20),
        primary_key=True
    )

    password = db.Column(
        db.Text,
        nullable=False
    )

    email = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )

    first_name = db.Column(
        db.String(30),
        nullable=False
    )

    last_name = db.Column(
        db.String(30),
        nullable=False
    )

    is_admin = db.Column(
               db.Boolean,
               nullable=False,
               default=False
    )



    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """ Creates a hash from password and returns new User instance. """

        hashed = bcrypt.generate_password_hash(password).decode("utf8")

        return cls(
            username=username,
            password=hashed,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

    @classmethod
    def authenticate(cls, username, password):
        """ Authenticate user from login form. """

        user = User.query.filter_by(username=username).one_or_none()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


class Note(db.Model):
    """ Note. """

    __tablename__ = "notes"

    id = db.Column(
         db.Integer,
         primary_key=True,
         autoincrement=True
    )
    title = db.Column(
            db.String(100),
            nullable=False
    )
    content = db.Column(
              db.Text,
              nullable=False
    )
    owner = db.Column(
            db.Text,
            db.ForeignKey("users.username"),
            nullable=False
    )

    user = db.relationship("User", backref="notes")


    def authorized(self, session_user):
        # Unauthorized:
        #      if session_user != username
        #   or if is_admin is Falue

        # Authorzied:
        #      
        return (session_user == self.user.username) or (self.user.is_admin is True)
            

