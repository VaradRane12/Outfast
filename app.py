from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config
from model import db
from routes.user_route import user_bp
from routes.product_route import product_bp
from routes.order_route import order_bp

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

db.init_app(app)

# Register Blueprints
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(product_bp, url_prefix="/product")
app.register_blueprint(order_bp, url_prefix="/order")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Flask-SQLite E-commerce API is running!"})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates tables if they don't exist
    app.run(debug=True)
