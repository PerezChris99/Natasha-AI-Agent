from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import timedelta
from modules.auth import User, db
from modules.commands import execute_command

# Initialize the app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Adjust for production
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and login manager
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Home Route
@app.route('/')
@login_required
def home():
    return render_template('dashboard.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect(url_for('home'))
        else:
            return 'Invalid credentials, please try again.'

    return render_template('login.html')

# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Command Route (Web Search, Open Apps, etc.)
@app.route('/execute', methods=['POST'])
@login_required
def execute():
    command = request.form.get('command')
    result = execute_command(command)
    return result

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
