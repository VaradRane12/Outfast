from flask import Blueprint, render_template, redirect, url_for, flash
from models import Cart, Product
from flask_login import login_required

checkout_bp = Blueprint('checkout', __name__)

@checkout_bp.route('/checkout/<username>', methods=["GET", "POST"])
@login_required
def checkout_summary(username):
    cart_items = Cart.query.filter_by(username=username).all()

    products_with_details = []
    total_price = 0
    total_quantity = 0

    for item in cart_items:
        product = Product.query.get(item.product_id)
        if product:
            products_with_details.append({
                "id": product.id,
                "name": product.productDisplayName,
                "price": product.price,
                "quantity": item.quantity,
                "total": product.price * item.quantity,
                "image_link": product.image_link
            })
            total_price += product.price * item.quantity
            total_quantity += item.quantity

    return render_template(
        "checkout.html",
        products=products_with_details,
        total_price=total_price,
        total_quantity=total_quantity,
        username=username
    )


@checkout_bp.route('/payment/<username>', methods=["GET", "POST"])
@login_required
def payment(username):
    cart_items = Cart.query.filter_by(username=username).all()

    if not cart_items:
        flash("Your cart is empty! Add some products first.", "warning")
        return redirect(url_for('cart_i'))

    total_price = sum(Product.query.get(item.product_id).price * item.quantity for item in cart_items)

    if total_price == 0:
        flash("Total price is zero. Add items to proceed with payment.", "warning")
        return redirect(url_for('cart_i'))

    # Simulate successful payment process
    flash("Payment successful! Your order has been placed.", "success")

    # Clear cart after payment
    Cart.query.filter_by(username=username).delete()

    return render_template("payment.html", username=username, total_price=total_price)
