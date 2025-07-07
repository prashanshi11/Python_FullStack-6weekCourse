from flask import Flask, render_template, request, session, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "123456789"

# MySQL Configuration
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "123456789"
app.config["MYSQL_DB"] = "registerlogin"

mysql = MySQL(app)

# Register Route
@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["name"]
        email = request.form["email"]
        password = request.form["pass"]
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tb (username, email, password) VALUES (%s, %s, %s)",
                    (username, email, password))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("login"))
    return render_template("register.html")

# Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["name"]
        password = request.form["pass"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM tb WHERE username = %s AND password = %s",
                    (username, password))
        account = cur.fetchone()
        cur.close()

        if account:
            session["loggedin"] = True
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", msg="Invalid credentials")
    return render_template("login.html")

# Dashboard Route
@app.route("/dashboard")
def dashboard():
    if "loggedin" in session:
        msg = f"Welcome {session['username']}!"
        return render_template("index.html", msg=msg)
    else:
        return redirect(url_for("login"))

# Logout Route
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
