from flask import Blueprint, render_template


bp = Blueprint('web', __name__)


@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/register')
def register():
    return render_template("register.html")

@bp.route("/login")
def login():
    return render_template("logon.html")

@bp.route("/report")
def report():
    return render_template("report.html")

@bp.route("/add_order")
def add_order():
    return "ERROR"

@bp.route("/export")
def export():
    return "ERROR"