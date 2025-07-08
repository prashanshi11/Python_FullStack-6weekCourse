from flask import Blueprint, request, render_template, redirect
from database import get_connection

contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO contact_messages (name, email, message) VALUES (%s, %s, %s)", 
                    (name, email, message))
        conn.commit()
        conn.close()

        return redirect('/contact')
    return render_template('contact.html')
