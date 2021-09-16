from cs50 import SQL
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session, request, redirect, url_for

db = SQL("sqlite:///plagiarism.db")

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

#class UploadForm(FlaskForm):

def text_file(filename):
    allowed_extensions = {'txt', 'doc', 'docx', 'odt', 'pdf', 'rtf', 'tex', 'wpd'}

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def password_duplicate(rows, password):
    for row in rows:
        if check_password_hash(row["hash"], password):
            return True
    return False


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = db.execute("SELECT * FROM users WHERE email = ?", email)
        if not user:
            raise ValidationError('There is no account with that email. You must register first.')