import random
import string
from flask import Blueprint, render_template, redirect, url_for, flash,request
from models import Cart, Product,OrderItem,Order
from flask_login import login_required
from models import db
checkout_bp = Blueprint('checkout', __name__)


@checkout_bp.route('/checkout/<username>', methods=["GET", "POST"])
def checkout_summary(username):
    # Fetch product details directly from Product table while retaining quantity from Cart
    cart_items = db.session.query(
        Product, Cart.quantity
    ).join(Product, Cart.product_id == Product.id).filter(Cart.username == username).all()

    if not cart_items:
        flash("Your cart is empty!", "warning")
        return redirect(url_for('cart.cart_i'))

    # Extract products and attach quantity
    products = []
    total_price = 0
    total_quantity = 0

    for product, quantity in cart_items:
        product_data = {
            "id": product.id,
            "name": product.productDisplayName,
            "price": product.price,
            "image_link": product.image_link,
            "quantity": quantity,
            "total": product.price * quantity
        }
        products.append(product_data)
        total_price += product_data["total"]
        total_quantity += quantity

    if request.method == "POST":
        # Generate an order number
        order_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        
        # Create and save order
        new_order = Order(username=username, total_price=total_price, total_quantity=total_quantity, order_number=order_number)
        db.session.add(new_order)
        db.session.commit()

        # Save ordered products
        order_items = [
            OrderItem(order_number=order_number, product_id=product["id"], quantity=product["quantity"], price=product["price"])
            for product in products
        ]
        db.session.bulk_save_objects(order_items)
        db.session.commit()

        # Clear cart
        Cart.query.filter_by(username=username).delete()
        db.session.commit()

        flash(f"Order {order_number} placed successfully!", "success")

        # ✅ Pass BOTH `username` and `order_number` to the payment route
        return redirect(url_for('checkout.payment', username=username, order_number=order_number))

    return render_template("checkout.html", products=products, total_price=total_price, total_quantity=total_quantity, username=username)

@checkout_bp.route('/payment/<username>/<order_number>', methods=["GET", "POST"])
@login_required
def payment(username, order_number):
    order = Order.query.filter_by(order_number=order_number, username=username).first()
    if not order:
        flash("Invalid order!", "danger")
        return redirect(url_for('checkout.checkout_summary', username=username))

    if request.method == "POST":
        flash(f"Payment for Order {order.order_number} successful!", "success") 
        return redirect(url_for('home.index')) 

    return render_template("payment_page.html", username=username, order=order)

@checkout_bp.route('/payment_success', methods=['POST'])
def payment_success():
    return render_template('thank_you.html')  
