from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from wtforms.fields.numeric import IntegerField, FloatField
from wtforms.fields.simple import EmailField, StringField, SubmitField
from wtforms.validators import DataRequired, Regexp, NumberRange, Email
from wtforms.widgets.core import NumberInput

from app.models.models import Product

CATEGORIES = [
    ('electronics', 'Электроника'),
    ('books', 'Книги'),
    ('clothing', 'Одежда'),
    ('food', 'Еда'),
    ('other', 'Другое'),
]

class ClientForm(FlaskForm):
    name = StringField()
    email = EmailField("Email", validators=[DataRequired()])
    phone = StringField("Телефон", validators=[
        DataRequired(message="Введите номер телефона"),
        Regexp(
            r'^\+?[\d\s\-\(\)]{10,}$',
            message="Номер телефона должен содержать только цифры, пробелы, дефисы, скобки и начинаться с +"
        )
    ])
    submit = SubmitField("Создать пользователя")


class OrderForm(FlaskForm):
    client_id = IntegerField('ID клиента', validators=[DataRequired(), NumberRange(min=1)])
    product_id = SelectField('Товар', coerce=int, validators=[DataRequired()])
    quantity = IntegerField('Количество', validators=[DataRequired(), NumberRange(min=1, max=999)])
    submit = SubmitField('Оформить заказ')

    def __init__(self, products, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product_id.choices = [(p.id, p.name) for p in products]

class ProductForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    price = FloatField('Цена', validators=[DataRequired(), NumberRange(min=0)])
    category = SelectField('Категория', choices=CATEGORIES, validators=[DataRequired()])
    submit = SubmitField("Добавить продукт")