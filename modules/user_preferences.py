import os
import json
import time
from datetime import datetime, time as dt_time

class UserPreferences:
    """Manages user preferences and settings for the voice assistant"""
    
    def __init__(self, config_file=None):
        """Initialize user preferences"""
        self.config_file = config_file or os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'preferences.json')
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        
        # Default preferences
        self.defaults = {
            "assistant_name": "Natasha",
            "wake_word": "natasha",
            "voice_rate": 175,
            "voice_volume": 0.9,
            "use_tts": True,
            "use_stt": True,
            "startup_greeting": True,
            "quiet_hours_enabled": False,
            "quiet_hours_start": "22:00",
            "quiet_hours_end": "07:00",
            "language": "en-US",
            "timezone": "local",
            "last_active_date": "",
            "daily_interactions": 0,
            "total_interactions": 0,
            "command_history": {}
        }
        
        # Load preferences
        self.preferences = self.load_preferences()
        
        # Update last active date if it's a new day
        current_date = datetime.now().strftime("%Y-%m-%d")
        if self.preferences.get("last_active_date") != current_date:
            self.preferences["last_active_date"] = current_date
            self.preferences["daily_interactions"] = 0
            self.save_preferences()
    
    def load_preferences(self):
        """Load preferences from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as file:
                    preferences = json.load(file)
                    # Make sure all default keys exist
                    for key, value in self.defaults.items():
                        if key not in preferences:
                            preferences[key] = value
                    return preferences
            except Exception as e:
                print(f"Error loading preferences: {e}")
        
        # If file doesn't exist or there's an error, create a new one with defaults
        self.save_preferences(self.defaults)
        return self.defaults.copy()
    
    def save_preferences(self, preferences=None):
        """Save preferences to file"""
        if preferences is None:
            preferences = self.preferences
        
        try:
            with open(self.config_file, 'w') as file:
                json.dump(preferences, file, indent=4)
        except Exception as e:
            print(f"Error saving preferences: {e}")
    
    def get_preference(self, key, default=None):
        """Get a preference value"""
        return self.preferences.get(key, default)
    
    def set_preference(self, key, value):
        """Set a preference value"""
        self.preferences[key] = value
        self.save_preferences()
    
    def is_quiet_hours(self):
        """Check if current time is within quiet hours"""
        if not self.preferences.get("quiet_hours_enabled", False):
            return False
        
        quiet_start_str = self.preferences.get("quiet_hours_start", "22:00")
        quiet_end_str = self.preferences.get("quiet_hours_end", "07:00")
        
        try:
            quiet_start = dt_time(
                *map(int, quiet_start_str.split(":")))
            quiet_end = dt_time(
                *map(int, quiet_end_str.split(":")))
            
            current = datetime.now().time()
            
            # Check if current time is in quiet hours
            if quiet_start <= quiet_end:
                # Normal case: quiet hours within the same day
                return quiet_start <= current <= quiet_end
            else:
                # Edge case: quiet hours span across midnight
                return current >= quiet_start or current <= quiet_end
        except Exception as e:
            print(f"Error checking quiet hours: {e}")
            return False
    
    def track_daily_activity(self):
        """Track daily activity"""
        self.preferences["daily_interactions"] += 1
        self.preferences["total_interactions"] += 1
        self.save_preferences()
    
    def track_command_usage(self, command):
        """Track command usage"""
        if "command_history" not in self.preferences:
            self.preferences["command_history"] = {}
            
        if command not in self.preferences["command_history"]:
            self.preferences["command_history"][command] = 0
            
        self.preferences["command_history"][command] += 1
        self.save_preferences()
    
    def get_most_used_commands(self, limit=5):
        """Get most frequently used commands"""
        command_history = self.preferences.get("command_history", {})
        sorted_commands = sorted(command_history.items(), key=lambda x: x[1], reverse=True)
        return sorted_commands[:limit]