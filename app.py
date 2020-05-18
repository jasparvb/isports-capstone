"""Flask app for iSports"""

from flask import Flask, request, redirect, render_template, flash, jsonify, session, g
from models import db, connect_db, User, Favorite, Follow
from forms import AddUserForm, LoginUserForm, AddFollow
from isports import get_top_news, get_all_news

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:41361@localhost/isports"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route("/")
def home():
    """Render homepage with top sports news headlines"""
    articles = get_top_news()
    return render_template("home.html", articles=articles)

############################################################################################
# Signup/Login/Logout
############################################################################################

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = AddUserForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect(f"/users/{user.username}")

    else:
        return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginUserForm()

    if form.validate_on_submit():
        user = User.login(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect(f"/news/{user.username}")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash("You have logged out", 'success')
    return redirect("/login")

############################################################################################
# User Profile
############################################################################################

@app.route('/user')
def show_user():
    """Show user profile."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")

    form = AddFollow()
    return render_template('user.html', form=form)

############################################################################################
# API
############################################################################################

@app.route('/api/follow', methods=['POST'])
def add_follow():
    """Add an item to follow"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")

    form = AddFollow()

    if form.validate_on_submit():
        name = form.name.data
        category = form.category.data
        sportsdb_id = form.sportsdb_id.data
        tb_image = form.tb_image.data

        follow = Follow(name=name, category=category, user_id=g.user.id, sportsdb_id=sportsdb_id, tb_image=tb_image)
        db.session.add(follow)
        db.session.commit()

    return redirect(f"/user")

@app.route("/follow/<follow_id>/delete", methods=['POST'])
def delete_follow(follow_id):
    """Delete follow"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")
    
    follow = Follow.query.get_or_404(follow_id)

    db.session.delete(follow)
    db.session.commit()

    return redirect(f"/user")


@app.route("/search")
def search_news():
    """Search sports news"""
    
    search = request.args["q"]
    print(search)
    articles = get_all_news(search)

    return render_template('search.html', articles=articles)
    
