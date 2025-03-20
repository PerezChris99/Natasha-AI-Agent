import os
import sys
import time
import datetime
import threading
import queue
import json
import re
import random

# Import modules
from modules.command_executor import CommandExecutor
from modules.user_preferences import UserPreferences
from modules.nlp_processor import NLPProcessor
from modules.language_translator import LanguageTranslator
from modules.api_key_manager import ApiKeyManager

# Text-to-speech and speech-to-text modules
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    print("pyttsx3 not available, text-to-speech will be disabled")
    TTS_AVAILABLE = False

try:
    import speech_recognition as sr
    STT_AVAILABLE = True
except ImportError:
    print("speech_recognition not available, speech-to-text will be disabled")
    STT_AVAILABLE = False

class VoiceAssistant:
    """Main voice assistant class that integrates all components"""
    
    def __init__(self):
        # Initialize components
        self.api_key_manager = ApiKeyManager()
        self.preferences = UserPreferences()
        self.nlp = NLPProcessor()
        self.translator = LanguageTranslator(self.api_key_manager)
        
        # Load assistant name from preferences
        self.name = self.preferences.get_preference("assistant_name", "Natasha")
        self.wake_word = self.preferences.get_preference("wake_word", self.name.lower())
        
        # Initialize command executor with reference to self
        self.executor = CommandExecutor(self)
        
        # Set up TTS and STT if available
        self._setup_tts()
        self._setup_stt()
        
        # Create response queue for async responses
        self.response_queue = queue.Queue()
        self.response_thread = None
        self.running = True
        
        # Welcome message
        self.startup_message = f"Hello, I am {self.name}, your voice assistant. How can I help you today?"

    def _setup_tts(self):
        """Set up Text-to-Speech"""
        self.tts_enabled = self.preferences.get_preference("use_tts", True) and TTS_AVAILABLE
        self.tts_engine = None
        
        if self.tts_enabled:
            try:
                self.tts_engine = pyttsx3.init()
                # Configure voice properties
                self.tts_engine.setProperty('rate', self.preferences.get_preference("voice_rate", 175))
                self.tts_engine.setProperty('volume', self.preferences.get_preference("voice_volume", 0.9))
                
                # Try to set a female voice if available
                voices = self.tts_engine.getProperty('voices')
                female_voice = None
                for voice in voices:
                    if "female" in voice.name.lower():
                        female_voice = voice.id
                        break
                
                if female_voice:
                    self.tts_engine.setProperty('voice', female_voice)
            except Exception as e:
                print(f"Error initializing TTS engine: {e}")
                self.tts_enabled = False

    def _setup_stt(self):
        """Set up Speech-to-Text"""
        self.stt_enabled = self.preferences.get_preference("use_stt", True) and STT_AVAILABLE
        self.recognizer = None
        
        if self.stt_enabled:
            try:
                self.recognizer = sr.Recognizer()
                # Adjust for ambient noise
                self.recognizer.dynamic_energy_threshold = True
            except Exception as e:
                print(f"Error initializing STT: {e}")
                self.stt_enabled = False

    def start(self):
        """Start the voice assistant"""
        # Start the response handler thread
        self.response_thread = threading.Thread(target=self._process_responses)
        self.response_thread.daemon = True
        self.response_thread.start()
        
        # Greet the user
        if self.preferences.get_preference("startup_greeting", True):
            self.respond(self.startup_message)
    
    def stop(self):
        """Stop the voice assistant"""
        self.running = False
        if self.response_thread and self.response_thread.is_alive():
            self.response_queue.put(None)  # Signal to stop the thread
            self.response_thread.join(timeout=1.0)
    
    def speak(self, text):
        """Convert text to speech"""
        if self.tts_enabled and self.tts_engine:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
                return True
            except Exception as e:
                print(f"TTS error: {e}")
                return False
        return False

    def listen(self, timeout=5):
        """Listen for user input via microphone"""
        if not self.stt_enabled or not self.recognizer:
            return None
            
        with sr.Microphone() as source:
            print("Listening...")
            try:
                audio = self.recognizer.listen(source, timeout=timeout)
                print("Processing speech...")
                
                # Attempt to recognize speech
                text = self.recognizer.recognize_google(audio)
                print(f"Recognized: {text}")
                return text
            except sr.WaitTimeoutError:
                print("Listen timeout")
                return None
            except sr.UnknownValueError:
                print("Could not understand audio")
                return None
            except sr.RequestError as e:
                print(f"Speech recognition error: {e}")
                return None
            except Exception as e:
                print(f"Error in speech recognition: {e}")
                return None

    def respond(self, response_text):
        """Queue a response to be processed"""
        if not response_text:
            return
            
        # Queue the response
        self.response_queue.put(response_text)
    
    def _process_responses(self):
        """Process responses from the queue"""
        while self.running:
            try:
                response = self.response_queue.get(timeout=1.0)
                if response is None:
                    break
                    
                # Print the response
                print(f"{self.name}: {response}")
                
                # Speak the response if TTS is enabled
                if not self.preferences.is_quiet_hours():
                    self.speak(response)
                    
                # Track interaction
                self.preferences.track_daily_activity()
                    
                # Mark the task as done
                self.response_queue.task_done()
            except queue.Empty:
                pass
            except Exception as e:
                print(f"Error processing response: {e}")

    def process_input(self, user_input):
        """Process user input and generate a response"""
        if not user_input:
            return
            
        # Print user input
        print(f"User: {user_input}")
        
        # Extract intent and entities
        intent = self.nlp.extract_intent(user_input)
        entities = self.nlp.extract_entities(user_input)
        
        # Check for custom patterns first
        custom_response = self.executor.handle_custom_pattern(user_input)
        if custom_response:
            self.respond(custom_response)
            return
            
        # Process commands based on intent
        if intent['intent'] == 'greeting':
            self.respond(f"Hello! How can I help you today?")
        elif intent['intent'] == 'farewell':
            self.respond("Goodbye! Have a nice day.")
        elif intent['intent'] == 'gratitude':
            self.respond("You're welcome! Is there anything else I can help you with?")
        elif intent['intent'] == 'help':
            help_text = self.executor.execute_command('help', None)
            self.respond(help_text)
        else:
            # Try to determine command and arguments
            # This is a simplified command parsing logic
            # In a real implementation, this would be more sophisticated
            command = self._extract_command(user_input, intent, entities)
            if command:
                cmd, args = command
                result = self.executor.execute_command(cmd, args)
                self.respond(result)
            else:
                self.respond("I'm not sure how to help with that. Can you be more specific?")
                
        # Track command usage
        if intent['intent'] != 'unknown':
            self.preferences.track_command_usage(intent['intent'])
            
    def _extract_command(self, text, intent, entities):
        """Extract command and arguments from text"""
        # Map intents to commands
        intent_to_command = {
            'weather': ('weather', 'local'),
            'time': ('get_time', None),
            'reminder': ('reminder', None),  # Will need to parse arguments
            'timer': ('timer', None),        # Will need to parse arguments
            'search': ('search', text.replace('search', '').strip()),
            'play': ('youtube', text.replace('play', '').strip()),
            'volume': ('volume', None),      # Will need to parse arguments
            'joke': ('joke', None),
            'calculation': ('math', None),   # Will need to parse the expression
            'help': ('help', None)
        }
        
        # Check if we can directly map the intent to a command
        if intent['intent'] in intent_to_command:
            cmd, default_args = intent_to_command[intent['intent']]
            
            # For some commands, we need to parse the arguments
            if cmd == 'timer':
                # Try to find a number followed by "minute(s)" or "second(s)"
                match = re.search(r'(\d+)\s*(minute|minutes|min|second|seconds|sec)', text.lower())
                if match:
                    amount = int(match.group(1))
                    unit = match.group(2)
                    if unit.startswith('sec'):
                        amount /= 60  # Convert to minutes
                    return (cmd, amount)
                return (cmd, 5)  # Default to 5 minutes
                
            elif cmd == 'reminder':
                # Try to parse "remind me to X in Y hours/minutes"
                match = re.search(r'remind\s+me\s+to\s+(.+?)\s+in\s+(\d+)\s*(hour|hours|minute|minutes|min)', text.lower())
                if match:
                    task = match.group(1)
                    amount = int(match.group(2))
                    unit = match.group(3)
                    if unit.startswith('min'):
                        amount /= 60  # Convert to hours
                    return (cmd, (task, amount))
                    
            elif cmd == 'volume':
                # Check for volume up/down/mute
                if 'up' in text.lower() or 'increase' in text.lower():
                    return (cmd, 'up')
                elif 'down' in text.lower() or 'decrease' in text.lower() or 'lower' in text.lower():
                    return (cmd, 'down')
                elif 'mute' in text.lower():
                    return (cmd, 'mute')
                    
            elif cmd == 'math':
                # Try to extract a mathematical expression
                # This is a simplified approach
                expression = text.lower()
                expression = expression.replace('calculate', '').replace('compute', '').replace('what is', '').strip()
                return (cmd, expression)
            
            # For commands with default arguments
            return (cmd, default_args)
            
        # If we can't map the intent directly, try some pattern matching
        if 'open' in text.lower() and len(text.split()) >= 2:
            app_name = text.lower().replace('open', '').strip()
            return ('app', app_name)
            
        if 'search for' in text.lower():
            query = text.lower().replace('search for', '').strip()
            return ('search', query)
            
        if 'play' in text.lower():
            content = text.lower().replace('play', '').strip()
            if 'spotify' in text.lower():
                content = content.replace('on spotify', '').strip()
                return ('spotify', content)
            else:
                content = content.replace('on youtube', '').strip()
                return ('youtube', content)
                
        # Default to a search if nothing else matches
        return ('search', text)

    def run_console(self):
        """Run the assistant in console mode"""
        self.start()
        
        print(f"\n=== {self.name} Voice Assistant ===")
        print("Type your commands or questions (type 'exit' to quit).")
        
        while self.running:
            try:
                user_input = input("\nYou: ")
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    self.respond("Goodbye!")
                    break
                    
                self.process_input(user_input)
            except KeyboardInterrupt:
                print("\nInterrupted by user.")
                break
            except Exception as e:
                print(f"Error: {e}")
                
        self.stop()
        print("Assistant stopped.")
