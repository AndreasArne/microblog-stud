"""
Contains forms used for authanticating a User
"""
from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User



class LoginForm(FlaskForm):
    """
    Form used to login a user
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')



class RegistrationForm(FlaskForm):
    """
    Form used to register a User
    """
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username): # pylint: disable=no-self-use
        """
        Check if username already exist
        """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            current_app.logger.debug(f"Username already exist. {user}")
            raise ValidationError('Please use a different username.')

    def validate_email(self, email): # pylint: disable=no-self-use
        """
        Check if email already exist
        """
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            current_app.logger.debug(f"Email already exist in a user. {user}")
            raise ValidationError('Please use a different email address.')
