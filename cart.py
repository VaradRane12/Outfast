from flask import Blueprint, render_template
from models import db, Product
from flask_login import login_required 
from sqlalchemy.sql import func

cart_bp = Blueprint('cart', __name__)
@cart_bp.route('/cart',methods=['GET', 'POST'])
@login_required
def cart_i():
    return render_template("cart.html")