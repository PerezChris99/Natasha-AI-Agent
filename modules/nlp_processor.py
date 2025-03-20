import re
import json
import os
import random
from collections import defaultdict

class NLPProcessor:
    """Natural Language Processing module for intent and entity extraction"""
    
    def __init__(self):
        """Initialize the NLP processor"""
        self.intents_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'intents.json')
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.intents_file), exist_ok=True)
        
        # Load or create intents
        self.intents = self.load_intents()
        
        # Compile regex patterns for faster matching
        self.compile_patterns()
    
    def load_intents(self):
        """Load intents from file or create default intents"""
        if os.path.exists(self.intents_file):
            try:
                with open(self.intents_file, 'r') as file:
                    return json.load(file)
            except Exception as e:
                print(f"Error loading intents: {e}")
        
        # Create default intents
        default_intents = {
            "intents": [
                {
                    "tag": "greeting",
                    "patterns": [
                        "hi", "hey", "hello", "good morning", "good afternoon", 
                        "good evening", "howdy", "what's up", "how are you"
                    ],
                    "responses": [
                        "Hello! How can I help you today?",
                        "Hi there! What can I do for you?",
                        "Hello! What can I assist you with?"
                    ]
                },
                {
                    "tag": "farewell",
                    "patterns": [
                        "bye", "goodbye", "see you later", "see you", 
                        "have a good day", "catch you later"
                    ],
                    "responses": [
                        "Goodbye! Have a nice day!",
                        "See you later!",
                        "Take care!"
                    ]
                },
                {
                    "tag": "gratitude",
                    "patterns": [
                        "thank you", "thanks", "appreciate it", "thank you so much", 
                        "thank you very much", "thanks a lot"
                    ],
                    "responses": [
                        "You're welcome!",
                        "Anytime!",
                        "Happy to help!"
                    ]
                },
                {
                    "tag": "help",
                    "patterns": [
                        "help", "help me", "i need help", "can you help me", 
                        "what can you do", "how do you work", "show commands",
                        "what are your features", "commands"
                    ],
                    "responses": [
                        "I can help with weather, time, reminders, searching the web, playing videos, and more. Just ask!"
                    ]
                },
                {
                    "tag": "weather",
                    "patterns": [
                        "weather", "what is the weather", "how's the weather", 
                        "weather forecast", "is it raining", "temperature",
                        "how hot is it", "how cold is it", "weather today",
                        "weather tomorrow", "will it rain", "is it sunny"
                    ],
                    "responses": []
                },
                {
                    "tag": "time",
                    "patterns": [
                        "what time is it", "current time", "tell me the time",
                        "what is the time", "time now", "what's the time",
                        "clock", "what time", "current date", "what is today's date",
                        "what day is it", "what is the date today"
                    ],
                    "responses": []
                },
                {
                    "tag": "reminder",
                    "patterns": [
                        "remind me", "set a reminder", "remind me to", 
                        "create a reminder", "set an alarm", "reminder"
                    ],
                    "responses": []
                },
                {
                    "tag": "timer",
                    "patterns": [
                        "set a timer", "timer for", "start timer", 
                        "set timer", "count down", "countdown"
                    ],
                    "responses": []
                },
                {
                    "tag": "search",
                    "patterns": [
                        "search for", "look up", "google", "find information", 
                        "search", "search about", "find"
                    ],
                    "responses": []
                },
                {
                    "tag": "play",
                    "patterns": [
                        "play", "play music", "play video", "play song", 
                        "youtube", "play on youtube", "spotify", "play on spotify"
                    ],
                    "responses": []
                },
                {
                    "tag": "volume",
                    "patterns": [
                        "volume up", "increase volume", "louder", 
                        "volume down", "decrease volume", "quieter",
                        "mute", "unmute", "set volume"
                    ],
                    "responses": []
                },
                {
                    "tag": "joke",
                    "patterns": [
                        "tell me a joke", "joke", "funny", "make me laugh", 
                        "tell me something funny", "humor me"
                    ],
                    "responses": []
                },
                {
                    "tag": "calculation",
                    "patterns": [
                        "calculate", "compute", "math", "what is", "add", "subtract", 
                        "multiply", "divide", "plus", "minus", "times", "divided by"
                    ],
                    "responses": []
                }
            ],
            "entities": [
                {
                    "tag": "time_unit",
                    "patterns": [
                        {"regex": "\\b(minute|minutes|min)\\b", "value": "minutes"},
                        {"regex": "\\b(second|seconds|sec)\\b", "value": "seconds"},
                        {"regex": "\\b(hour|hours|hr)\\b", "value": "hours"},
                        {"regex": "\\b(day|days)\\b", "value": "days"}
                    ]
                },
                {
                    "tag": "location",
                    "patterns": [
                        {"regex": "\\bin ([a-zA-Z\\s]+)\\b", "group": 1},
                        {"regex": "\\bfor ([a-zA-Z\\s]+)\\b", "group": 1}
                    ]
                },
                {
                    "tag": "number",
                    "patterns": [
                        {"regex": "\\b(\\d+)\\b", "group": 1}
                    ]
                }
            ]
        }
        
        # Save default intents
        try:
            with open(self.intents_file, 'w') as file:
                json.dump(default_intents, file, indent=4)
        except Exception as e:
            print(f"Error saving default intents: {e}")
        
        return default_intents
    
    def compile_patterns(self):
        """Compile regex patterns for faster matching"""
        self.compiled_patterns = {}
        
        # Compile intent patterns
        for intent in self.intents["intents"]:
            tag = intent["tag"]
            patterns = intent["patterns"]
            self.compiled_patterns[tag] = [re.compile(f"\\b{pattern}\\b", re.IGNORECASE) for pattern in patterns]
        
        # Compile entity patterns
        self.compiled_entity_patterns = {}
        for entity in self.intents.get("entities", []):
            tag = entity["tag"]
            self.compiled_entity_patterns[tag] = []
            
            for pattern in entity["patterns"]:
                regex_pattern = pattern["regex"]
                self.compiled_entity_patterns[tag].append({
                    "regex": re.compile(regex_pattern, re.IGNORECASE),
                    "value": pattern.get("value"),
                    "group": pattern.get("group", 0)
                })
    
    def extract_intent(self, text):
        """Extract intent from text"""
        if not text:
            return {"intent": "unknown", "confidence": 0}
            
        best_match = {"intent": "unknown", "confidence": 0}
        
        # Count how many patterns match for each intent
        matches = defaultdict(int)
        total_patterns = 0
        
        for intent, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                if pattern.search(text.lower()):
                    matches[intent] += 1
            total_patterns += len(patterns)
        
        # Calculate confidence for each intent with matches
        for intent, match_count in matches.items():
            # Simple confidence calculation based on number of matching patterns
            confidence = match_count / max(1, len(self.compiled_patterns[intent]))
            
            if confidence > best_match["confidence"]:
                best_match = {"intent": intent, "confidence": confidence}
        
        return best_match
    
    def extract_entities(self, text):
        """Extract entities from text"""
        if not text:
            return {}
            
        entities = {}
        
        for entity_type, patterns in self.compiled_entity_patterns.items():
            entities[entity_type] = []
            
            for pattern_info in patterns:
                regex = pattern_info["regex"]
                group = pattern_info.get("group", 0)
                default_value = pattern_info.get("value")
                
                for match in regex.finditer(text):
                    try:
                        value = match.group(group)
                        if default_value:
                            value = default_value
                            
                        # For numbers, convert to integer if possible
                        if entity_type == "number":
                            try:
                                value = int(value)
                            except ValueError:
                                pass
                                
                        entities[entity_type].append({
                            "value": value,
                            "start": match.start(group),
                            "end": match.end(group)
                        })
                    except IndexError:
                        continue
        
        return entities
    
    def get_random_response(self, intent_tag):
        """Get a random response for a given intent tag"""
        for intent in self.intents["intents"]:
            if intent["tag"] == intent_tag and intent.get("responses"):
                return random.choice(intent["responses"])
        return None
