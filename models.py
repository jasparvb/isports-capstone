"""Models for iSports app."""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)


# MODELS
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    username = db.Column(db.String(50), unique=True, nullable=False)

    password = db.Column(db.Text, nullable=False)

    email = db.Column(db.String(50), nullable=True)

    favorites = db.relationship( 'Favorite', backref="user", cascade="all, delete")

    follows = db.relationship( 'Follow', backref="users", cascade="all, delete")
  
    def __repr__(self):
        u = self
        return f"<User username={u.username} email={u.email}>"

    @classmethod
    def signup (cls, username, password, email):
        """Sign up a user with hashed password and return user"""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(username=username, password=hashed_utf8, email=email)
        db.session.add(user)
        return user

    @classmethod
    def login (cls, username, password):
        """Check to see if user exists and return user if valid, else return False"""
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


class Favorite(db.Model):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.Text, nullable=False)

    url = db.Column(db.Text, nullable=False)

    image_url = db.Column(db.Text, nullable=False)

    published_at = db.Column(db.DateTime, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), nullable=False)
 
    def __repr__(self):
        u = self
        return f"<Favorite title={u.title}>"


class Follow(db.Model):
    __tablename__ = 'follows'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.Text, nullable=False)

    sportsdb_id = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), nullable=False)

    category = db.Column(db.String(50), nullable=False)

    tb_image = db.Column(db.Text, nullable=True)

    def __repr__(self):
        u = self
        return f"<Follow name={u.name}>"
