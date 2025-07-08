from flask import Flask
from routes.auth import auth_bp
from routes.product import product_bp
from routes.cart import cart_bp
from routes.checkout import checkout_bp
from routes.contact import contact_bp

app = Flask(__name__)

# Secret key for sessions (keep this safe!)
app.secret_key = 'your_super_secret_key'

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(product_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(checkout_bp)
app.register_blueprint(contact_bp)

# Static + template folders (Flask auto-detects if in same folder)
# OR set manually: app = Flask(__name__, static_folder='static', template_folder='templates')

if __name__ == '__main__':
    app.run(debug=True)
