from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from wtforms.fields.numeric import IntegerField, FloatField
from wtforms.fields.simple import EmailField, StringField, SubmitField
from wtforms.validators import DataRequired, Regexp, NumberRange, Email
from wtforms.widgets.core import NumberInput


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
    name = StringField("Имя клиента", validators=[
        DataRequired(message="Введите имя клиента")
    ])

    email = StringField("Email клиента", validators=[
        DataRequired(message="Введите email клиента"),
        Email(message="Некорректный email")
    ])

    product_id = IntegerField("ID продукта", validators=[
        DataRequired(message="Введите ID продукта"),
        NumberRange(min=1, message="ID продукта должен быть положительным числом")
    ])

    quantity = IntegerField("Количество", validators=[
        DataRequired(message="Укажите количество"),
        NumberRange(min=1, max=999, message="Количество должно быть от 1 до 999")
    ], widget=NumberInput(min=1, max=999))

    total_price = FloatField("Общая стоимость", validators=[
        DataRequired(message="Укажите общую стоимость"),
        NumberRange(min=0.01, message="Стоимость должна быть больше 0")
    ])

    status = SelectField("Статус заказа", choices=[
        ('pending', 'Ожидает обработки'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен')
    ], validators=[DataRequired(message="Выберите статус заказа")])

    submit = SubmitField("Создать заказ")

class ProductForm(FlaskForm):
    name = StringField("Название продукта", validators=[
        DataRequired(message="Введите название продукта")
    ])

    price = FloatField("Цена", validators=[
        DataRequired(message="Укажите цену продукта"),
        NumberRange(min=0.01, message="Цена должна быть больше 0")
    ])

    category = StringField("Категория", validators=[
        # Не обязательное поле
    ])

    submit = SubmitField("Добавить продукт")  # 👈 Не забудьте импортировать SubmitField!