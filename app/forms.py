from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    nickname = StringField('nickname', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
