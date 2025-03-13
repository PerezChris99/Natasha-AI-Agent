from flask import Flask
from modules.auth import auth_bp
from modules.commands import commands_bp
from modules.spotify_integration import spotify_bp
from modules.youtube_integration import youtube_bp

def create_app():
    """Create and configure the Flask app."""
    app = Flask(__name__)

    # Configuration settings (you can load from a config file or environment variables)
    app.config['SECRET_KEY'] = 'your_secret_key'  # Change this in a real app
    app.config['SESSION_COOKIE_NAME'] = 'your_session_cookie_name'
    
    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(commands_bp)
    app.register_blueprint(spotify_bp)
    app.register_blueprint(youtube_bp)
    
    return app
