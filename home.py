from flask import Blueprint, render_template
from models import db, Product  # Use db from models.py
from sqlalchemy.sql import func

home_bp = Blueprint('home', __name__)

@home_bp.route('/', methods=['GET', 'POST'])
def index():
    excluded_categories = ["Innerwear", "Loungewear and Nightwear"]
    random_products = (
        Product.query
        .filter(~Product.subCategory.in_(excluded_categories))
        .order_by(func.random())  # Randomize order
        .limit(9)  # Limit to 9 results
        .all()
)

    offers = [
    {"image_link": "static/assets/banner2.jpeg"},
    {"image_link": "static/assets/banner3.jpeg"},
]
    return render_template('index.html', products=random_products,offers=offers)
