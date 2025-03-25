from flask import Flask
from models import db 
from home import home_bp 
import os
app = Flask(__name__,template_folder="templates")
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'store1.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

app.register_blueprint(home_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True,port  = 8001)
