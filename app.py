from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from functools import wraps

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-change-this'   # needed for sessions
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'   # reuse your existing DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Define the Contact model (maps to 'contacts' table)
class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    message = db.Column(db.String(500), nullable=False)

# Create tables 
with app.app_context():
    db.create_all()

# ---------- Admin authentication (password protection) ----------
def login_required(role="ADMIN"):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not session.get('admin_logged_in'):
                return redirect(url_for('admin_login'))
            return f(*args, **kwargs)
        return decorated
    return wrapper

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Change these to any credentials you want
        if username == 'admin' and password == 'javajam123':
            session['admin_logged_in'] = True
            return redirect('/admin')
        else:
            flash('Invalid credentials', 'danger')
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect('/')
# ----------------------------------------------------------------

# Custom ModelView that requires login
class SecureModelView(ModelView):
    def is_accessible(self):
        return session.get('admin_logged_in', False)

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin_login'))

# Setup Flask-Admin
admin = Admin(app, name='Admin Dashboard', template_mode='bootstrap4')
admin.add_view(SecureModelView(Contact, db.session))

# ---------- Your existing routes ----------
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

@app.route('/submit_form', methods=['POST'])
def submit_form():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    message = request.form['message']

    # Save using SQLAlchemy (instead of raw sqlite3)
    new_contact = Contact(name=name, email=email, phone=phone, message=message)
    db.session.add(new_contact)
    db.session.commit()

    return "Message saved successfully!"

if __name__ == '__main__':
    app.run(debug=True)
