from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()  # Initialize SQLAlchemy
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
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


    

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), db.ForeignKey('users.username'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)  # Assuming product ID
    quantity = db.Column(db.Integer, default=1)

    user = db.relationship('User', backref=db.backref('cart', lazy=True))


