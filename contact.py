from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required,current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db

contact_bp = Blueprint('contact', __name__)

@contact_bp.route("/contact",methods = ["GET","POST"])
def contact():
    return render_template("contactusoutfast.html")