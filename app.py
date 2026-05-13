from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Create database
def init_db():
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            message TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

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

    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO contacts (name, email, phone, message)
        VALUES (?, ?, ?, ?)
    ''', (name, email, phone, message))

    conn.commit()
    conn.close()

    return "Message saved successfully!"

if __name__ == '__main__':
    app.run(debug=True)