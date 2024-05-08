from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flaskblog.models import User
from wtforms.validators import ValidationError
from flask import flash
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed

# inheritance,
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(min=5, max=20)
                                                   ],)
    email = StringField('E-mail', validators=[DataRequired(), Email(), ])
    password = PasswordField('Password', validators=[DataRequired()])
    conf_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password') ])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            flash('Username taken', 'danger')
            raise ValidationError('Username taken')


    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        flash('Email taken', 'danger')
        if user:
            raise ValidationError('Email taken')
    
class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember')
    submit = SubmitField('Log In')

class UpdateForm(FlaskForm):
    username = StringField('New Username', validators=[DataRequired(),
                                                   Length(min=5, max=20)
                                                   ],)
    email = StringField('New E-mail', validators=[DataRequired(), Email(), ])
    image_file = FileField('Update Profile Picture', 
                           validators= [FileAllowed(['jpeg','png','jpg'] )]
                           )
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username: 
            user = User.query.filter_by(username = username.data).first()
            if user:
                flash('Username taken', 'danger')
                raise ValidationError('Username taken')


    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            flash('Email taken', 'danger')
            if user:
                raise ValidationError('Email taken')