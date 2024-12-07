import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.secret_key = 'your_secret_key'  # Secret key for session management and flash messages

DATABASE = 'requests.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

def init_db():
    with app.app_context():
        db = get_db()
        # Create tables if they don't exist
        db.execute('''
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                request_details TEXT NOT NULL,
                file_path TEXT NOT NULL
            )
        ''')
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        db.commit()

init_db()

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Connect to the database and check if the user exists
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

        if user and check_password_hash(user['password'], password):
            # Successful login, redirect to the profile or dashboard
            return redirect(url_for('profile'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Hash the password before storing it
        hashed_password = generate_password_hash(password)

        # Connect to the database and check if the email already exists
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

        if user:
            flash('Email is already registered', 'error')
            return render_template('register.html')

        # Insert the new user into the database
        db.execute('''
            INSERT INTO users (username, email, password)
            VALUES (?, ?, ?)
        ''', (username, email, hashed_password))
        db.commit()

        flash('Registration successful, please login', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)
