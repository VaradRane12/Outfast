from flask import Blueprint, render_template,request
from models import Product


category_bp = Blueprint('category', __name__)


@category_bp.route('/category', methods=["GET",'POST'])
def categories():
    # Fetch unique (Master Category, Sub Category, Product Type) combinations
    category_data = Product.query.with_entities(
        Product.masterCategory, Product.subCategory, Product.articleType
    ).distinct().order_by(Product.masterCategory, Product.subCategory, Product.articleType).all()

    # Structure data into a nested dictionary
    category_tree = {}
    for master, sub, article in category_data:
        if master not in category_tree:
            category_tree[master] = {}
        if sub not in category_tree[master]:
            category_tree[master][sub] = []
        category_tree[master][sub].append(article)

    return render_template("category.html", category_tree=category_tree)

@category_bp.route("/filter_category",methods = ["GET","POST"])
def filter_category():
    master = request.args.get('master', None)
    sub = request.args.get('sub', None)
    article = request.args.get('article', None)
    print(master,sub,article)
    return render_template("filtered_results.html", master=master, sub=sub, article=article)
