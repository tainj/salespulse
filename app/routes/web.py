from itertools import product

from flask import Blueprint, render_template, redirect, url_for, flash

from app.db import get_db
from app.form.form import ClientForm, OrderForm, ProductForm
from app.models.models import Client

bp = Blueprint('web', __name__)


@bp.route("/")
def home():
    order_form = OrderForm()
    client_form = ClientForm()
    product_form = ProductForm()
    return render_template('home.html',
                           add_order_form=order_form, add_client_form=client_form,
                           add_product_form=product_form)

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
            return redirect(url_for('web.add_client'))  # или redirect('/')

        except Exception as e:
            db_sess.rollback()  # ← ОБЯЗАТЕЛЬНО! Откат при ошибке
            flash("Произошла ошибка при добавлении клиента.")
            return render_template('home.html', form=form)

        finally:
            db_sess.close()
    return redirect("/")

@bp.route("/export")
def export():
    return "ERROR"

@bp.route("/add_product")
def add_product():
    return "ERROR"