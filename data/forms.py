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
    submit = SubmitField('Подтвердить')


class MapHeadForm(FlaskForm):
    city = StringField('Населённый пункт', validators=[InputRequired()])
    name = StringField('Названия заметки', validators=[InputRequired()])
    submit = SubmitField('Подтвердить')


class MapBodyForm(FlaskForm):
    place = StringField('Место', validators=[InputRequired()])
    text = StringField('Текст заметки')
    type = BooleanField('Посещено ?')
    submit = SubmitField('Подтвердить')


class MapChangeForm(FlaskForm):
    place = StringField('Место', validators=[InputRequired()])
    text = StringField('Текст заметки')
    type = BooleanField('Посещено ?')
    submit = SubmitField('Подтвердить')

