from collections import namedtuple
from datetime import datetime
import logging

from flask import Blueprint, render_template, redirect, flash, request
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from app.db import get_db
from app.form.form import ClientForm, OrderForm, ProductForm, ClientFilterForm, ProductFilterForm, OrderFilterForm
from app.models.models import Client, Product, Order
import plotly.express as px

bp = Blueprint('web', __name__)
logger = logging.getLogger(__name__)


@bp.route("/")
def home():
    db_sess = get_db()

    # получение параметров
    selected_country = request.args.get('country')
    selected_category = request.args.get('category')
    selected_client_id = request.args.get('client_id')

    # фильтр по категории
    products_query = db_sess.query(
        Product.id,
        Product.name,
        Product.price,
        Product.category,
        func.coalesce(func.sum(Order.quantity), 0).label('total_sold'),  # сколько продано
        func.coalesce(func.sum(Order.total_price), 0.0).label('total_revenue')  # выручка
    ).outerjoin(Order, Product.id == Order.product_id) \
        .group_by(Product.id) \
        .order_by(Product.name)
    if selected_category:
        products_query = products_query.filter(Product.category == selected_category)
    products = products_query.all()

    # фильтр заказов
    orders_query = db_sess.query(Order)
    if selected_client_id and selected_client_id.isdigit():
        orders_query = orders_query.filter(Order.client_id == int(selected_client_id))
    orders = orders_query.all()

    # фильтр клиентов
    clients_query = db_sess.query(
        Client.id,
        Client.firstname,
        Client.lastname,
        Client.email,
        Client.phone,
        Client.country,
        func.count(Order.id).label('order_count')
    ).outerjoin(Order, Client.id == Order.client_id) \
        .group_by(Client.id) \
        .order_by(Client.lastname, Client.firstname)

    if selected_country:
        clients_query = clients_query.filter(Client.country == selected_country)
    clients = clients_query.all()

    order_form = OrderForm(db_sess.query(Product).all())
    client_form = ClientForm()
    product_form = ProductForm()
    filter_form_clients = ClientFilterForm()
    filter_form_product = ProductFilterForm()
    filter_form_orders = OrderFilterForm()

    return render_template('home.html',
                           add_order_form=order_form,
                           add_client_form=client_form,
                           add_product_form=product_form,
                           clients=clients,
                           products=products,
                           orders=orders,
                           filter_form_clients=filter_form_clients,
                           filter_form_product=filter_form_product,
                           filter_form_orders=filter_form_orders,
                           selected_country=selected_country,
                           selected_category=selected_category,
                           selected_client_id=selected_client_id)

@bp.route("/report")
def report():
    session = get_db()  # ваша сессия

    stats = session.query(
        func.count(Order.id).label('total_orders'),
        func.sum(Order.total_price).label('total_revenue'),
        func.count(func.distinct(Order.client_id)).label('unique_clients')
    ).first()

    total_orders = stats.total_orders or 0
    total_revenue = float(stats.total_revenue or 0)
    unique_clients = stats.unique_clients or 0
    avg_ticket = round(total_revenue / total_orders, 2) if total_orders > 0 else 0.0

    top_clients = session.query(
        Client.firstname,
        Client.lastname,
        func.sum(Order.total_price).label('revenue')
    ).join(Order, Client.id == Order.client_id) \
     .group_by(Client.id) \
     .order_by(func.sum(Order.total_price).desc()) \
     .limit(5) \
     .all()

    top_client_names = [f"{c.firstname} {c.lastname}" for c in top_clients]
    top_client_revenue = [float(r) for _, _, r in top_clients]

    fig_top_clients = px.bar(
        x=top_client_names,
        y=top_client_revenue,
        labels={'x': 'Клиент', 'y': 'Выручка (₽)'},
        title='🏆 Топ-5 клиентов по выручке',
        color_discrete_sequence=['#2E86AB']
    )
    fig_top_clients.update_layout(
        xaxis_tickangle=-45,
        template='plotly_white'
    )
    top_clients_chart = fig_top_clients.to_html(full_html=False)

    category_sales = session.query(
        Product.category,
        func.sum(Order.total_price).label('revenue')
    ).join(Order, Product.id == Order.product_id) \
     .group_by(Product.category) \
     .order_by(func.sum(Order.total_price).desc()) \
     .all()

    categories = [cat for cat, _ in category_sales]
    category_revenue = [float(rev) for _, rev in category_sales]

    fig_pie = px.pie(
        names=categories,
        values=category_revenue,
        title='🎯 Доля продаж по категориям',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    pie_chart = fig_pie.to_html(full_html=False)

    daily_revenue = session.query(
        func.date(Order.created_at).label('date'),
        func.sum(Order.total_price).label('revenue')
    ).group_by(func.date(Order.created_at)) \
     .order_by('date') \
     .all()

    if daily_revenue:
        dates = [row.date for row in daily_revenue]
        revenues = [float(row.revenue) for row in daily_revenue]
        fig_line = px.line(
            x=dates,
            y=revenues,
            labels={'x': 'Дата', 'y': 'Выручка (₽)'},
            title='📈 Динамика выручки по дням'
        )
        fig_line.update_layout(template='plotly_white')
        sales_chart = fig_line.to_html(full_html=False)
    else:
        sales_chart = "<div class='text-center text-muted'>Нет данных для построения графика.</div>"

    top_products = session.query(
        Product.name,
        func.sum(Order.quantity).label('total_sold')
    ).join(Order, Product.id == Order.product_id) \
     .group_by(Product.id) \
     .order_by(func.sum(Order.quantity).desc()) \
     .limit(5) \
     .all()

    product_names = [name for name, _ in top_products]
    product_sold = [int(q) for _, q in top_products]

    fig_top_products = px.bar(
        x=product_names,
        y=product_sold,
        labels={'x': 'Товар', 'y': 'Количество проданных штук'},
        title='🔥 Топ-5 самых продаваемых товаров',
        color_discrete_sequence=['#C74A4A']
    )
    fig_top_products.update_layout(
        xaxis_tickangle=-45,
        template='plotly_white'
    )
    top_products_chart = fig_top_products.to_html(full_html=False)

    OrderItem = namedtuple('OrderItem', ['order', 'firstname', 'lastname', 'product_name'])

    orders = [
        OrderItem(o, fn, ln, pn)
        for o, fn, ln, pn in session.query(
            Order, Client.firstname, Client.lastname, Product.name
        ).join(Client, Order.client_id == Client.id)
         .join(Product, Order.product_id == Product.id)
         .order_by(Order.created_at.desc())
         .all()
    ]

    country_revenue = session.query(
        Client.country,
        func.sum(Order.total_price).label('revenue')
    ).join(Order, Client.id == Order.client_id) \
        .group_by(Client.country) \
        .order_by(func.sum(Order.total_price).desc()) \
        .all()

    country_names = [country for country, _ in country_revenue]
    country_revenues = [float(r) for _, r in country_revenue]

    if country_revenue:
        fig_country = px.pie(
            names=country_names,
            values=country_revenues,
            title='🌍 Выручка по странам клиентов',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_country.update_traces(textposition='inside', textinfo='percent+label')
        country_revenue_chart = fig_country.to_html(full_html=False)
    else:
        country_revenue_chart = "<div class='text-center text-muted'>Нет данных по странам.</div>"

    return render_template("report.html",
        sales_chart=sales_chart,
        top_clients_chart=top_clients_chart,
        pie_chart=pie_chart,
        top_products_chart=top_products_chart,

        total_orders=total_orders,
        total_revenue=round(total_revenue, 2),
        avg_ticket=avg_ticket,
        unique_clients=unique_clients,
        orders=orders,
        country_revenue_chart=country_revenue_chart
    )


@bp.route("/add_order", methods=['GET', 'POST'])
def add_order():
    logging.info("Add order")
    db_sess = get_db()  # ваша сессия SQLAlchemy

    # получаем список всех продуктов
    products = db_sess.query(Product).all()
    form = OrderForm(products)

    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                # получаем id клиента
                client_id = form.client_id.data

                # проверяем, существует ли клиент с таким ID
                client = db_sess.query(Client).filter(Client.id == client_id).first()

                if not client:
                    flash(f"Клиент с ID {client_id} не найден. Пожалуйста, проверьте данные.", "danger")
                    return redirect("/")

                # получаем остальные данные
                product_id = form.product_id.data
                quantity = form.quantity.data
                create_at = form.created_at.data

                # проверяем, существует ли товар
                product = db_sess.query(Product).filter(Product.id == product_id).first()
                if not product:
                    flash("Выбранный товар не найден.", "danger")
                    return render_template('add_order.html', form=form, products=products)

                # создаём заказ
                order = Order(
                    client_id=client_id,
                    product_id=product_id,
                    quantity=quantity,
                    total_price=product.price * quantity,
                    created_at=create_at
                )

                db_sess.add(order)
                db_sess.commit()

                flash(f"Заказ успешно оформлен! Клиент: {client.lastname} {client.firstname}, Товар: {product.name}, Количество: {quantity}", "success")
                return

            except SQLAlchemyError as e:
                db_sess.rollback()
                flash("Ошибка при сохранении заказа. Попробуйте позже.", "danger")
                logger.error("failed to get form order", "error", e)
            except Exception as e:
                db_sess.rollback()
                flash("Неожиданная ошибка. Обратитесь в поддержку.", "danger")
                logger.error("failed to get form order", "error", e)
            finally:
                return redirect("/")

        else:
            flash("Пожалуйста, исправьте ошибки в форме.", "warning")
            return redirect("/")

    return redirect("/")


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
                firstname=form.firstname.data,
                lastname=form.lastname.data,
                email=form.email.data,
                phone=form.phone.data,
                country=form.country.data
            )
            db_sess.add(client)
            db_sess.commit()
            flash("Клиент добавлен!")

        except Exception as e:
            db_sess.rollback()
            flash("Произошла ошибка при добавлении клиента.")
            logger.error("failed to get form client", "error", e)
        finally:
            db_sess.close()
            return redirect('/')

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

        except Exception as e:
            db_sess.rollback()
            flash("Произошла ошибка при добавлении продукта. Попробуйте ещё раз.")
            logger.error("failed to get form product", "error", e)
        finally:
            db_sess.close()
            return redirect("/")