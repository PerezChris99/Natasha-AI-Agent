# Natasha Voice Assistant

A modular and extensible voice assistant framework built in Python.

## Features

- Text-to-speech and speech-to-text capabilities
- Command-based interaction
- Natural language processing
- Multi-language support
- User preference learning and adaptation
- API key management with encryption
- Timer and reminder functionality
- Web search integration
- Application management
- Weather and news retrieval
- Smart home device control (simulation)
- Mathematical calculations
- Language translation

## Installation

1. Clone this repository:
   ```
   git clone https://your-repo-url/natasha.git
   cd natasha
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Run the setup:
   ```
   python main.py --setup
   ```

## Usage

### Command Line

Run the assistant in console mode:
```
python main.py --console
```

### Options

- `--no-tts`: Disable text-to-speech
- `--no-stt`: Disable speech-to-text
- `--console`: Run in console mode
- `--setup`: Run initial setup
- `--debug`: Enable debug logging

## Commands

Natasha supports many commands, including:

- **Web Search**: "Search for [query]"
- **Open Applications**: "Open [app name]"
- **YouTube**: "Play [video] on YouTube"
- **Spotify**: "Play [song] on Spotify"
- **Timers**: "Set a timer for [minutes] minutes"
- **Reminders**: "Remind me to [task] in [hours] hours"
- **Weather**: "What's the weather in [location]?"
- **News**: "Tell me the latest news about [topic]"
- **Jokes**: "Tell me a joke"
- **Time and Date**: "What time is it?" or "What's today's date?"
- **Math**: "Calculate [expression]"
- **System Status**: "What's my system status?"

## Project Structure

```
natasha/
├── main.py                 # Main entry point
├── modules/                # Core modules
│   ├── voice_assistant.py  # Main assistant class
│   ├── command_executor.py # Command execution
│   ├── nlp_processor.py    # Natural language processing
│   ├── user_preferences.py # User preferences management
│   ├── api_key_manager.py  # Secure API key management
│   └── language_translator.py # Multi-language support
├── data/                   # User data storage
├── config/                 # Configuration files
└── logs/                   # Log files
```

## Extending Functionality

You can extend Natasha's capabilities by modifying the `command_executor.py` file. Add new methods to the `CommandExecutor` class and update the `execute_command` method to map commands to your new functions.

## Dependencies

- Python 3.7+
- pyttsx3 (for text-to-speech)
- SpeechRecognition (for speech-to-text)
- nltk (for natural language processing)
- spacy (for advanced NLP)
- transformers (optional, for advanced language tasks)
- googletrans (for translation)
- cryptography (for API key encryption)

## License

This project is licensed under the MIT License - see the LICENSE file for details.


