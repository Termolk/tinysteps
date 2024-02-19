from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.choices import RadioField, SelectField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import SubmitField, HiddenField
from wtforms.validators import DataRequired, Length


class BookForm(FlaskForm):
    name = StringField('Вас зовут', validators=[DataRequired(), Length(min=2, max=30)])
    phone = StringField('Ваш телефон', validators=[DataRequired(), Length(min=11, max=12)])
    submit = SubmitField('Записаться на пробный урок')

    clientWeekday = HiddenField('')
    clientTime = HiddenField('')
    clientTeacher = HiddenField('')


class RequestForm(FlaskForm):
    goal = RadioField(
        'goal',
        choices=[('travel', 'Для путешествий'), ('learn', 'Для школы'), ('work', 'Для работы'),
                 ('move', 'Для переезда')],
        default='travel'
    )
    time = RadioField(
        'time',
        choices=[('1-2', '1-2 часа в неделю'), ('3-5', '3-5 часов в неделю'), ('5-7', '5-7 часов в неделю'),
                 ('7-10', '7-10 часов в неделю')],
        default='1-2'
    )
    name = StringField('Вас зовут', validators=[DataRequired(), Length(min=2, max=30)])
    phone = StringField('Ваш телефон', validators=[DataRequired(), Length(min=11, max=12)])
    submit = SubmitField('Найдите мне преподователя')


class SortForm(FlaskForm):
    selectField = SelectField(
        'Sort settings',
        choices=[('0', 'В случайном порядке'), ('1', 'Сначала дорогие'), ('2', 'Сначала недорогие'),
                 ('3', 'Сначала лучшие по рейтингу')],
        default=0
    )
    submit = SubmitField('Сортировать')
