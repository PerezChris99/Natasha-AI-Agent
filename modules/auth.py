from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Initialize the database
db = SQLAlchemy()

# User model for authentication
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Store hashed passwords
    
    def __repr__(self):
        return f'<User {self.username}>'

# Function to create the database tables (if they don't exist yet)
def create_db():
    with app.app_context():
        db.create_all()
