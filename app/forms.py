from flask_wtf import Form
from wtforms import TextField, PasswordField, IntegerField, StringField
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

class RegisterDoctorForm(Form):
    permit_number = IntegerField(
        'Permit Number', validators=[DataRequired(), Length(min=7, max=7)]
    )
    first_name = StringField(
        'First Name', validators=[DataRequired(), Length(min=2, max=40)]
    )
    last_name = StringField(
        'Last Name', validators=[DataRequired(), Length(min=2, max=40)]
    )
    speciality = StringField(
        'Speciality', validators=[DataRequired(), Length(min=2, max=40)]
    )
    city = StringField(
        'City', validators=[DataRequired(), Length(min=2, max=40)]
    )
