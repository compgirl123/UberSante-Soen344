from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length


class RegisterForm(Form):
    name = TextField(
        'Username', validators=[DataRequired(), Length(min=6, max=25)]
    )
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
        EqualTo('password', message='Passwords must match')]
    )


class LoginForm(Form):
    name = TextField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


class ForgotForm(Form):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
class PatientRegisterForm(Form):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
    name = TextField(
        'First Name', validators=[DataRequired(), Length(min=6, max=25)]
    )
    lastName= TextField(
        'Last Name', validators=[DataRequired(), Length(min=6, max=25)]
    )
    phoneNumber= TextField(
        'Phone Number', validators=[DataRequired(), Length(min=9, max=9)]
    )    
    address = TextField(
        'Address', validators=[DataRequired(), Length(min=6, max=40)]
    )
    birthDay = TextField(
        'Birth Day', validators=[DataRequired(), Length(min=6, max=40)]
    )
    gender = TextField(
        'Gender', validators=[DataRequired(), Length(min=6, max=40)]
    )
    healthCardNumber =TextField(
        'Health Card Number', validators=[DataRequired(), Length(min=6, max=40)]
    )