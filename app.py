from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, NumberRange
from sqlalchemy.sql.expression import func
import os
app = Flask(__name__,template_folder="templates")
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'store1.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    category = StringField('Category')
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Add Product')

class OrderForm(FlaskForm):
    product_id = SelectField('Product', coerce=int, validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Place Order')

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100))
    stock = db.Column(db.Integer, default=0)
# with app.app_context():
#     products = Product.query.all()
#     print(products)  # This should not be an empty list
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
class Product(db.Model):
    __tablename__ = 'products'
    __table_args__ = {'extend_existing': True}  # Allow redefining

    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(10), nullable=False)
    masterCategory = db.Column(db.Text)
    subCategory = db.Column(db.Text)
    articleType = db.Column(db.String(100))
    baseColour = db.Column(db.String(20))
    season = db.Column(db.String(50))
    year = db.Column(db.Integer)
    usage = db.Column(db.String, default="0")
    productDisplayName = db.Column(db.Text)
    price = db.Column(db.Integer, nullable=True)  
    discountedPrice = db.Column(db.Integer, nullable=True)  
    brandName = db.Column(db.String(100), nullable=True)  
    myntraRating = db.Column(db.Float, nullable=True)  
    image_link = db.Column(db.String)  # Ensure this exists in your database


@app.route('/', methods=['GET', 'POST'])
def index():
    random_products = Product.query.order_by(func.random()).limit(9).all()  # Fetch 9 random products
    return render_template('index.html', products=random_products)  # Pass to Jinja template
@app.route("/add_product",methods = ["GET","POST"])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            category=form.category.data,
            stock=form.stock.data
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('index'))
    products = Product.query.all()
    return render_template('Add_prod.html', form=form, products=products)

@app.route('/order', methods=['GET', 'POST'])
def order():
    form = OrderForm()
    form.product_id.choices = [(p.id, p.name) for p in Product.query.all()]
    if form.validate_on_submit():
        product = Product.query.get(form.product_id.data)
        if product and product.stock >= form.quantity.data:
            product.stock -= form.quantity.data
            order = Order(product_id=form.product_id.data, quantity=form.quantity.data)
            db.session.add(order)
            db.session.commit()
            flash('Order placed successfully!', 'success')
        else:
            flash('Not enough stock!', 'danger')
        return redirect(url_for('order'))
    return render_template('order.html', form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

