from flask import Blueprint, jsonify, render_template,request,url_for,redirect
from models import db, Product
from flask_login import login_required, current_user
from sqlalchemy.sql import func
cart_bp = Blueprint('cart', __name__)
from flask import request, jsonify, session
from models import db, Cart, Product, User  # Import necessary models
from auth import auth_bp

@cart_bp.route('/add_to_cart', methods=["GET",'POST'])
@login_required

def add_to_cart():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))  # Manually redirect
    product_id = request.form.get('product_id') or request.json.get('product_id')
    username = current_user.username  # Get logged-in user from session
    

    
    if not product_id:
        return jsonify({'error': 'No product ID provided'}), 400

    # Check if the product exists
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    # Check if the item is already in the cart
    existing_cart_item = Cart.query.filter_by(username=username, product_id=product_id).first()

    if existing_cart_item:
        existing_cart_item.quantity += 1  # Increase quantity if already in cart
    else:
        new_cart_item = Cart(username=username, product_id=product_id, quantity=1)
        db.session.add(new_cart_item)

    db.session.commit()  # Save changes to the database

    return jsonify({"success":True,'message': "added Succesfully to Cart"})

@cart_bp.route('/cart', methods=['GET', 'POST'])
@login_required
def cart_i():
    username = current_user.username

    # Fetch all cart items for the user
    cart_items = Cart.query.filter_by(username=username).all()

    # Get product details for each item in the cart
    products_with_quantity = []
    for item in cart_items:
        product = Product.query.get(item.product_id)  # Fetch product details
        if product:
            products_with_quantity.append({
                'id': product.id,
                'name': product.productDisplayName,
                'price': product.price,
                'image_link': product.image_link,
                'quantity': item.quantity  # Include quantity from Cart table
            })

    return render_template("cart.html", products=products_with_quantity)
@cart_bp.route("/update_cart_quantity",methods = ["POST"]) 
def update_cart():
    data = request.get_json()
    product_id = data.get("product_id")
    action = data.get("action")
    username = current_user.username
    existing_cart_item = Cart.query.filter_by(username=username, product_id=product_id).first()
    if action == 'increase' and existing_cart_item:
        existing_cart_item.quantity +=1
    if action == 'decrease' and existing_cart_item:
        existing_cart_item.quantity -=1
    db.session.commit()  # Save changes to the database

    return jsonify({"success": True})

@cart_bp.route("/remove_from_cart",methods = ["POST"]) 
def remove_cart():
    data = request.get_json()
    product_id = data.get("product_id")
    action = data.get("action")
    username = current_user.username
    cart_item = Cart.query.filter_by(username=username, product_id=product_id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
    return jsonify({"success": True})