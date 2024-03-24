from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[InputRequired()])
    password = PasswordField('Пароль', validators=[InputRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    surname = StringField('Фамилия')
    name = StringField('Имя')
    email = EmailField('Почта', validators=[InputRequired()])
    password = PasswordField('Пароль', validators=[InputRequired()])
    password_again = PasswordField('Ещё раз пароль', validators=[InputRequired()])
    submit = SubmitField('submit')


class MapForm(FlaskForm):
    city = StringField('Населённый пункт')
    place = StringField('Место')
    text = StringField('Текст заметки')
    submit = SubmitField('submit')

