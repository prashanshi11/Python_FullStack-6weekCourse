from flask import Blueprint, render_template, session, redirect

checkout_bp = Blueprint('checkout', __name__)

@checkout_bp.route('/checkout')
def checkout():
    cart = session.get('cart', [])
    if not cart:
        return redirect('/products')
    return render_template('checkout.html', cart=cart)
