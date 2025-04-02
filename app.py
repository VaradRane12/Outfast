from flask import Flask,url_for,redirect
from flask_login import LoginManager
from flask_login import logout_user

from models import db, User
from home import home_bp
from auth import auth_bp
from cart import cart_bp
from search import search_bp
from category import category_bp



import os
from flask_cors import CORS



app = Flask(__name__, template_folder="templates")
CORS(app)  # Enable CORS globally

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'store1.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)
app.register_blueprint(home_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(cart_bp)
app.register_blueprint(category_bp)
app.register_blueprint(search_bp)




# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"
@login_manager.user_loader

def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("auth.login"))

@app.route('/test')
def test():
    return redirect(url_for('auth.login'))  # ✅ Works inside a request contextAAAAAAAAAAAAA

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
    app.run(debug=True, port=8001)
