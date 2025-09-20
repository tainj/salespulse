from flask import Blueprint, render_template, redirect, url_for, flash

from app.db import get_db
from app.form.form import ClientForm, OrderForm, ProductForm
from app.models.models import Client, Product

bp = Blueprint('web', __name__)


@bp.route("/")
def home():
    # получение данных
    db_sess = get_db()
    clients = db_sess.query(Client).all()
    products = db_sess.query(Product).all()

    # создание форм
    order_form = OrderForm(products)
    client_form = ClientForm()
    product_form = ProductForm()
    return render_template('home.html',
                           add_order_form=order_form, add_client_form=client_form,
                           add_product_form=product_form, clients=clients, products=products)

@bp.route("/report")
def report():
    return render_template("report.html")

@bp.route("/add_order")
def add_order():
    return "ERROR"


@bp.route("/add_client", methods=['GET', 'POST'])
def add_client():
    form = ClientForm()

    if form.validate_on_submit():
        db_sess = get_db()
        try:
            # проверяем, чтобы пользователя не было с таким же email
            existing = db_sess.query(Client).filter(Client.email == form.email.data).first()
            if existing:
                flash("Этот email уже зарегистрирован.")
                return redirect("/")

            # создаём клиента
            client = Client(
                name=form.name.data,
                email=form.email.data,
                phone=form.phone.data,
            )
            db_sess.add(client)
            db_sess.commit()
            flash("Клиент добавлен!")
            return redirect('/')

        except Exception as e:
            db_sess.rollback()
            flash("Произошла ошибка при добавлении клиента.")
            return redirect("/")

        finally:
            db_sess.close()
    return redirect("/")

@bp.route("/export")
def export():
    return "ERROR"

@bp.route("/add_product", methods=["GET", "POST"])
def add_product():
    form = ProductForm()

    if form.validate_on_submit():
        db_sess = get_db()
        try:
            existing = db_sess.query(Product).filter(Product.name == form.name.data).first()
            if existing:
                flash("Продукт с таким названием уже существует.")
                return redirect("/")

            # создаём новый продукт
            product = Product(
                name=form.name.data,
                price=form.price.data,
                category=form.category.data,
            )
            db_sess.add(product)
            db_sess.commit()
            flash("Продукт успешно добавлен!")
            return redirect("/")

        except Exception as e:
            db_sess.rollback()
            flash("Произошла ошибка при добавлении продукта. Попробуйте ещё раз.")
            return redirect("/")

        finally:
            db_sess.close()

    return redirect("/")