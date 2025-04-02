from flask import Blueprint, request, jsonify, render_template
from models import db, Product

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').strip()
    if not query:
        return render_template("search.html", query=query, results=[])

    results = Product.query.filter(
        (Product.productDisplayName.ilike(f"%{query}%")) | (Product.brandName.ilike(f"%{query}%"))
    ).all()

    return render_template("search.html", query=query, results=results)
