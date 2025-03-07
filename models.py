from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Initialize SQLAlchemy

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

    def __repr__(self):
        return f"<Product {self.name}>"
