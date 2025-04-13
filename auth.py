from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required,current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db,Order,OrderItem,Product
from collections import defaultdict
auth_bp = Blueprint('auth', __name__)
@auth_bp.route("/order_history", methods=["GET", "POST"])
def order_history():
    user = current_user.username
    orders = Order.query.filter_by(username=user).all()
    dic = {}
    for i in orders:
        dic[i.order_number] = OrderItem.query.filter_by(order_number=i.order_number).all()

    ht_dic = defaultdict(list)
    for order_num, items in dic.items():
        for item in items:
            product = Product.query.filter_by(id=item.product_id).first()
            ht_dic[order_num].append([product.image_link, product.productDisplayName, product.price])

    return render_template("order_history.html", ht_dic=ht_dic, orders=orders)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose another.', 'danger')
            return redirect(url_for('auth.register'))

        # Hash the password and store it in the database
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('home.index'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home.index'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html', user=current_user)



@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.index'))
