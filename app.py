from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SECRET KEY
app.config['SECRET_KEY'] = 'bookstore_secret'

# DATABASE CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'

db = SQLAlchemy(app)

# =========================
# DATABASE MODEL
# =========================

class Contact(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    email = db.Column(db.String(100))

    phone = db.Column(db.String(50))

    message = db.Column(db.Text)

# CREATE DATABASE
with app.app_context():
    db.create_all()

# =========================
# ADMIN PASSWORD
# =========================

ADMIN_PASSWORD = "admin123"

# =========================
# CUSTOM ADMIN LOGIN
# =========================

class MyAdminIndexView(AdminIndexView):

    @expose('/', methods=['GET', 'POST'])
    def index(self):

        if request.method == 'POST':

            password = request.form.get('password')

            if password == ADMIN_PASSWORD:

                return super(MyAdminIndexView, self).index()

            return '''
                <h2>Wrong Password</h2>
                <a href="/admin">Try Again</a>
            '''

        return '''
            <form method="POST" style="margin:50px;">
                <h2>Admin Login</h2>

                <input type="password" name="password" placeholder="Enter Password">

                <button type="submit">Login</button>
            </form>
        '''

# =========================
# FLASK ADMIN
# =========================

admin = Admin(
    app,
    name='Book Store Admin',
    index_view=MyAdminIndexView()
)

admin.add_view(ModelView(Contact, db.session))

# =========================
# ROUTES
# =========================

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/books')
def books():
    return render_template('books.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# =========================
# FORM SUBMISSION
# =========================

@app.route('/submit_form', methods=['POST'])
def submit_form():

    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    message = request.form['message']

    new_message = Contact(
        name=name,
        email=email,
        phone=phone,
        message=message
    )

    db.session.add(new_message)

    db.session.commit()

    return redirect('/contact')

# =========================

if __name__ == '__main__':
    app.run(debug=True)
