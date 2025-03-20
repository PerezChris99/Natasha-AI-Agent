import os
import re
import time
import datetime
import random
import json
import webbrowser
import subprocess
import threading
import requests
import math
from urllib.parse import quote_plus

class CommandExecutor:
    """Execute commands based on user input"""
    
    def __init__(self, assistant):
        """Initialize command executor"""
        self.assistant = assistant
        self.reminders = []
        self.timers = []
        self.custom_patterns = self._load_custom_patterns()
        
        # Start background timer for checking reminders
        self.reminder_thread = threading.Thread(target=self._check_reminders_loop, daemon=True)
        self.reminder_thread.start()
    
    def _load_custom_patterns(self):
        """Load custom patterns for regex matching"""
        # These are regex patterns that can directly trigger actions without NLP
        patterns = [
            # Basic conversation patterns
            {
                "pattern": r"\b(what is|what'?s) your name\b",
                "action": "self._respond_with_name"
            },
            {
                "pattern": r"\b(who are|who're) you\b",
                "action": "self._respond_with_identity"
            },
            {
                "pattern": r"\b(how are|how're) you\b",
                "action": "self._respond_with_status"
            },
            # Custom commands
            {
                "pattern": r"\bshutdown\b",
                "action": "self._shutdown"
            },
            {
                "pattern": r"\brestart\b",
                "action": "self._restart"
            }
        ]
        
        # Compile the patterns for faster matching
        for pattern in patterns:
            pattern["compiled"] = re.compile(pattern["pattern"], re.IGNORECASE)
        
        return patterns
    
    def handle_custom_pattern(self, text):
        """Handle custom regex patterns"""
        for pattern in self.custom_patterns:
            if pattern["compiled"].search(text):
                action_name = pattern["action"]
                # Call the corresponding method
                if action_name.startswith("self."):
                    method = getattr(self, action_name[5:])
                    return method()
        return None
    
    def execute_command(self, command, args):
        """Execute a command with given arguments"""
        command_method = f"_cmd_{command}"
        
        if hasattr(self, command_method):
            try:
                method = getattr(self, command_method)
                return method(args)
            except Exception as e:
                return f"Error executing command {command}: {str(e)}"
        else:
            return f"Unknown command: {command}"
    
    def _respond_with_name(self):
        """Respond with assistant name"""
        return f"My name is {self.assistant.name}."
    
    def _respond_with_identity(self):
        """Respond with assistant identity"""
        return f"I am {self.assistant.name}, your voice assistant. I'm here to help you with various tasks."
    
    def _respond_with_status(self):
        """Respond with assistant status"""
        responses = [
            "I'm doing well, thank you! How can I help you?",
            "I'm functioning properly, thanks for asking. How can I assist you?",
            "All systems operational! What can I do for you today?",
            "I'm great! Ready to help with whatever you need."
        ]
        return random.choice(responses)
    
    def _shutdown(self):
        """Shutdown the assistant"""
        self.assistant.running = False
        return "Shutting down. Goodbye!"
    
    def _restart(self):
        """Restart the assistant"""
        # This would typically be implemented by the main application
        return "Restarting is not implemented yet."
    
    def _cmd_help(self, args):
        """Show help about available commands"""
        help_text = (
            f"Hi! I'm {self.assistant.name}, your voice assistant. Here are things I can help you with:\n\n"
            "- Weather information: 'What's the weather like?'\n"
            "- Time and date: 'What time is it?'\n"
            "- Reminders: 'Remind me to call John in 2 hours'\n"
            "- Timers: 'Set a timer for 5 minutes'\n"
            "- Web searches: 'Search for recipes for lasagna'\n"
            "- Play media: 'Play Bohemian Rhapsody on YouTube'\n"
            "- Volume control: 'Turn the volume up/down'\n"
            "- Jokes: 'Tell me a joke'\n"
            "- Math calculations: 'What is 15 times 7?'\n"
            "- Open applications: 'Open calculator'\n\n"
            "You can also ask me questions like 'What's your name?' or 'How are you?'"
        )
        return help_text
    
    def _cmd_weather(self, location):
        """Get weather information"""
        if not location or location == 'local':
            location = "current location"
            
        # Weather API call would go here - this is a placeholder
        try:
            if self.assistant.api_key_manager.get_api_key("openweathermap"):
                api_key = self.assistant.api_key_manager.get_api_key("openweathermap")
                return self._get_weather_from_api(location, api_key)
            else:
                return f"I'd check the weather for {location}, but I don't have an API key for the weather service."
        except Exception as e:
            return f"Sorry, I couldn't get the weather information for {location}. Error: {str(e)}"
    
    def _get_weather_from_api(self, location, api_key):
        """Get weather data from OpenWeatherMap API"""
        # This is a placeholder for actual API call
        return f"The weather in {location} is currently sunny with a temperature of 72°F (22°C"