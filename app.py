from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, NumberRange

app = Flask(__name__,template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
app.config['SECRET_KEY'] = 'secretkey'
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

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
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
    return render_template('index.html', form=form, products=products)

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

