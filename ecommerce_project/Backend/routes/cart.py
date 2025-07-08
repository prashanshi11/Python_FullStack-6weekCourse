from flask import Blueprint, session, redirect, render_template, request
from database import get_connection

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart')
def view_cart():
    cart = session.get('cart', [])
    return render_template('cart.html', cart=cart)

@cart_bp.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))

    # Simulate a cart in session
    cart = session.get('cart', [])
    cart.append({'product_id': product_id, 'quantity': quantity})
    session['cart'] = cart

    return redirect('/cart')
