from datetime import datetime

from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import DateTimeField
from wtforms.fields.numeric import IntegerField, FloatField
from wtforms.fields.simple import EmailField, StringField, SubmitField
from wtforms.validators import DataRequired, Regexp, NumberRange, Email, Optional

CATEGORIES = [
    ('electronics', 'Электроника'),
    ('books', 'Книги'),
    ('clothing', 'Одежда'),
    ('food', 'Еда'),
    ('other', 'Другое'),
]

COUNTRIES = [
    ('Russia', 'Россия'),
    ('USA', 'США'),
    ('Germany', 'Германия'),
    ('France', 'Франция'),
    ('China', 'Китай'),
    ('Japan', 'Япония'),
    ('UK', 'Великобритания'),
    ('Canada', 'Канада'),
    ('Australia', 'Австралия'),
    ('Brazil', 'Бразилия'),
    ('India', 'Индия'),
]

COUNTRIES_FOR_FORM = [
    ('', '— Все страны —'),
    ('Russia', 'Россия'),
    ('USA', 'США'),
    ('Germany', 'Германия'),
    ('France', 'Франция'),
    ('China', 'Китай'),
    ('Japan', 'Япония'),
    ('UK', 'Великобритания'),
    ('Canada', 'Канада'),
    ('Australia', 'Австралия'),
    ('Brazil', 'Бразилия'),
    ('India', 'Индия'),
]

class ClientForm(FlaskForm):
    firstname = StringField('Имя', validators=[DataRequired()])
    lastname = StringField('Фамилия', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Телефон', validators=[
        DataRequired(),
        Regexp(r'^\+?[\d\s\-\(\)]{10,}$', message="Неверный формат телефона")
    ])
    country = SelectField('Страна', coerce=str, validators=[DataRequired()])
    submit = SubmitField('Создать пользователя')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.country.choices = COUNTRIES


class ClientFilterForm(FlaskForm):
    country = SelectField(
        'Фильтр по стране',
        coerce=str,
        choices=COUNTRIES_FOR_FORM,
        validators=[Optional()]
    )
    submit = SubmitField('Получить')


class OrderForm(FlaskForm):
    client_id = IntegerField('ID клиента', validators=[DataRequired(), NumberRange(min=1)])
    product_id = SelectField('Товар', coerce=int, validators=[DataRequired()])
    quantity = IntegerField('Количество', validators=[DataRequired(), NumberRange(min=1, max=999)])
    created_at = DateTimeField(
        'Дата и время заказа',
        format='%Y-%m-%dT%H:%M',
        default=datetime.now,
        validators=[DataRequired()]
    )
    submit = SubmitField('Оформить заказ')

    def __init__(self, products, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product_id.choices = [(p.id, p.name) for p in products]

class OrderFilterForm(FlaskForm):
    client_id = IntegerField(
        'Фильтр по ID клиента',
        validators=[
            Optional(),
            NumberRange(min=1, message="ID клиента должен быть больше 0")
        ],
        render_kw={"placeholder": "Введите ID клиента"}
    )
    submit = SubmitField('Получить')

class ProductForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    price = FloatField('Цена', validators=[DataRequired(), NumberRange(min=0)])
    category = SelectField('Категория', choices=CATEGORIES, validators=[DataRequired()])
    submit = SubmitField("Добавить продукт")

class ProductFilterForm(FlaskForm):
    category = SelectField(
        'Фильтр по категории',
        coerce=str,
        choices=[('', '— Все категории —')] + CATEGORIES,
        validators=[Optional()]
    )
    submit = SubmitField('Получить')