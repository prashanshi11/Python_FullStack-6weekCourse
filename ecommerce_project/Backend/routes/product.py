from flask import Blueprint, render_template
from database import get_connection

product_bp = Blueprint('product', __name__)

@product_bp.route('/')
def index():
    return render_template('index.html')

@product_bp.route('/products')
def show_products():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    conn.close()
    return render_template('products.html', products=products)

@product_bp.route('/product/<int:product_id>')
def product_details(product_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cur.fetchone()
    conn.close()
    return render_template('product-details.html', product=product)
