# Natasha - Personal Virtual Assistant

Natasha is a web-based personal virtual assistant that can perform various tasks including voice commands, web searches, application management, and media playback.

## Features

- **Voice Command Recognition**: Convert speech to text and execute commands
- **Web Search**: Search the web using voice or text commands
- **Application Management**: Open applications via commands
- **Media Playback**: 
  - Play local media files
  - Integrate with Spotify for music streaming
  - Play YouTube videos
- **User Authentication**: Secure login system to protect your assistant

## Requirements

- Python 3.8+
- Flask
- SpeechRecognition
- pyttsx3
- Flask-SQLAlchemy
- Flask-Login
- python-dotenv
- Spotify API credentials (for Spotify integration)
- Other dependencies as specified in `requirements.txt`

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd Natasha
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your credentials:
   ```
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   SPOTIFY_REDIRECT_URI=your_spotify_redirect_uri
   SECRET_KEY=your_flask_secret_key
   ```

4. Initialize the database:
   ```
   flask db init
   flask db migrate
   flask db upgrade
   ```

## Usage

1. Start the application:
   ```
   python app.py
   ```

2. Navigate to `http://127.0.0.1:5000` in your web browser
3. Log in to access the dashboard
4. Use the interface to:
   - Issue voice commands
   - Search the web
   - Control media playback
   - Open applications

## Voice Commands

Examples of voice commands you can use:
- "Search for [query]"
- "Open [application name]"
- "Play [song name] on Spotify"
- "Play [video name] on YouTube"

## Project Structure

- `app.py`: Main application file
- `modules/`: Contains integration modules for different services
- `voice/`: Speech-to-text and text-to-speech functionality
- `templates/`: HTML templates for the web interface
- `static/`: CSS, JavaScript, and other static files


