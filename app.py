from flask import Flask, render_template, jsonify, request
from modules.commands import perform_web_search, open_application, play_media
from modules.spotify_integration import play_spotify_track
from modules.youtube_integration import play_youtube_video
from voice.speech_to_text import recognize_speech
from voice.text_to_speech import speak
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import webbrowser
import os

# Initialize the Flask app and other extensions
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# User model for authentication
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Create the database if it doesn't exist
with app.app_context():
    db.create_all()

# Load the user by ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid login credentials', 'danger')

    return render_template('login.html')

# Route for logging out
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Route for dashboard (only accessible after login)
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Web search functionality
@app.route('/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('query')
    if query:
        return redirect(f'https://www.google.com/search?q={query}')
    return 'No search query provided.'

# Open application functionality
@app.route('/open', methods=['GET'])
@login_required
def open_application():
    app_name = request.args.get('app')
    if app_name == 'browser':
        webbrowser.open('https://www.google.com')
        return 'Opening browser...'
    return 'Application not recognized.'

# Play media functionality
@app.route('/play', methods=['GET'])
@login_required
def play_media():
    media_type = request.args.get('media')
    if media_type == 'music':
        os.system('start music.mp3')  # Adjust with actual media file path or player
        return 'Playing music...'
    elif media_type == 'movie':
        os.system('start movie.mp4')  # Adjust with actual media file path or player
        return 'Playing movie...'
    return 'Media not recognized.'

@app.route('/voice/command', methods=['GET'])
def voice_command():
    # Get the voice command via speech recognition
    command = recognize_speech()
    
    if command:
        # Respond with speech (Text-to-Speech)
        speak(f"You said: {command}")
        
        # Return the command as JSON response
        return jsonify({"command": command})
    else:
        return jsonify({"command": None})

@app.route('/action/search', methods=['GET'])
def search():
    query = request.args.get('q')
    if query:
        perform_web_search(query)
        return jsonify({"status": "success"})
    return jsonify({"status": "failure"})

@app.route('/action/open', methods=['GET'])
def open():
    app_name = request.args.get('app')
    if app_name:
        open_application(app_name)
        return jsonify({"status": "success", "app": app_name})
    return jsonify({"status": "failure"})

@app.route('/action/play', methods=['GET'])
def play():
    media_name = request.args.get('media')
    if media_name:
        play_media(media_name)
        return jsonify({"status": "success", "media": media_name})
    return jsonify({"status": "failure"})

app.route('/action/play/spotify', methods=['GET'])
def play_spotify():
    track_name = request.args.get('track')
    if track_name:
        play_spotify_track(track_name)
        return jsonify({"status": "success", "track": track_name})
    return jsonify({"status": "failure"})

@app.route('/action/play/youtube', methods=['GET'])
def play_youtube():
    video_url = request.args.get('url')
    if video_url:
        play_youtube_video(video_url)
        return jsonify({"status": "success", "video": video_url})
    return jsonify({"status": "failure"})

if __name__ == '__main__':
    app.run(debug=True)
