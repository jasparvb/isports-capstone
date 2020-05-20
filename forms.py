from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, HiddenField
from wtforms.validators import InputRequired, Optional, Email

class AddUserForm(FlaskForm):
    """Form for signing up a user."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[Optional(), Email()], render_kw={"placeholder": "(Optional)"})

class LoginUserForm(FlaskForm):
    """Form for logging in a user."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class AddFollow(FlaskForm):
    """Form for adding a follow."""

    name = StringField("Name", validators=[InputRequired()], render_kw={"placeholder": "(example: Lionel Messi)"})
    category = HiddenField("Category")
    sportsdb_id = HiddenField("Dbid")
    tb_image = HiddenField("Thumb")
