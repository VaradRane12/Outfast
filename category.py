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
    article = request.args.get('article', None)
    sub = request.args.get('sub', None)
    master = request.args.get('master', None)
    print((article,sub,master))
    # Prioritized filtering: Article > Sub > Master
    if article:
        products = Product.query.filter_by(articleType=article).all()
    elif sub:
        products = Product.query.filter_by(subCategory=sub).all()
    elif master:
        products = Product.query.filter_by(masterCategory=master).all()
    else:
        products = Product.query.all()  # No filters applied, return all products
    print(products[0].productDisplayName)
    return render_template("filtered_results.html", products=products)



