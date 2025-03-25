from flask import Blueprint, render_template
from models import db, Product  # Use db from models.py
from sqlalchemy.sql import func

home_bp = Blueprint('home', __name__)

@home_bp.route('/', methods=['GET', 'POST'])
def index():
    random_products = Product.query.order_by(func.random()).limit(9).all()
    offers = [
    {"image_link": "static/assets/sale_banner1.jpg"},
    {"image_link": "static/assets/banner2.jpeg"},
    {"image_link": "static/assets/banner3.jpeg"},
]
    return render_template('index.html', products=random_products,offers=offers)
