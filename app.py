from flask import Flask
from flask_login import LoginManager
from models import db, User
from home import home_bp
from auth import auth_bp
import os

app = Flask(__name__, template_folder="templates")
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'store1.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register Blueprints
app.register_blueprint(home_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8001)
