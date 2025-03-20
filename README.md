# Natasha - Personal Virtual Assistant

Natasha is a desktop virtual assistant that can perform various tasks including voice commands, web searches, application management, and media playback.

## Features

- **Voice Command Recognition**: Convert speech to text and execute commands
- **Web Search**: Search the web using voice or text commands
- **Application Management**: Open applications via commands
- **Media Playback**: 
  - Play local media files
  - Integrate with Spotify for music streaming
  - Play YouTube videos


## Requirements

python for desktop apps

## Installation

1. Create a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

2. Install PyAudio dependencies (Windows):
```bash
pip install pipwin
pipwin install pyaudio
```

3. Install other requirements:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your credentials:
   ```bash
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   SPOTIFY_REDIRECT_URI=your_spotify_redirect_uri
   SECRET_KEY=your_flask_secret_key
   ```

5

## Running the Application

```bash
python desktop_app.py
```

## Usage

1. Start the application:
   ```bash
   python app.py


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


