from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import StringField, EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired

from server import photos


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


class MapBodyForm1(FlaskForm):
    place = StringField('Место', validators=[InputRequired()])
    text = StringField('Текст заметки')
    type = BooleanField('Посещено ?')
    submit = SubmitField('Подтвердить')


class MapBodyForm2(MapBodyForm1):
    name = SelectField('Название набора заметок', choices=[])


class UploadForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(photos, 'Image only!'),
                      FileRequired('File was empty!')])
    submit = SubmitField('Upload')
