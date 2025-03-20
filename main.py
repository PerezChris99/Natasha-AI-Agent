#!/usr/bin/env python3
"""
Natasha Voice Assistant
A modular and extensible voice assistant framework
"""

import os
import sys
import argparse
from modules.voice_assistant import VoiceAssistant

def setup_environment():
    """Set up the environment for the assistant"""
    # Create necessary directories
    os.makedirs(os.path.join(os.path.dirname(__file__), "data"), exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(__file__), "config"), exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(__file__), "logs"), exist_ok=True)
    
    # Add modules directory to path if needed
    modules_dir = os.path.join(os.path.dirname(__file__), "modules")
    if modules_dir not in sys.path:
        sys.path.append(modules_dir)

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Natasha Voice Assistant")
    parser.add_argument("--no-tts", action="store_true", help="Disable text-to-speech")
    parser.add_argument("--no-stt", action="store_true", help="Disable speech-to-text")
    parser.add_argument("--console", action="store_true", help="Run in console mode")
    parser.add_argument("--setup", action="store_true", help="Run initial setup")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    return parser.parse_args()

def run_setup():
    """Run initial setup for the assistant"""
    from modules.user_preferences import UserPreferences
    from modules.api_key_manager import ApiKeyManager
    
    print("=== Natasha Voice Assistant Setup ===")
    
    # Setup preferences
    prefs = UserPreferences()
    name = input("What would you like to name your assistant? [Natasha]: ")
    if name:
        prefs.set_preference("assistant_name", name)
    
    wake_word = input(f"Set a wake word for your assistant (default: {prefs.get_preference('assistant_name').lower()}): ")
    if wake_word:
        prefs.set_preference("wake_word", wake_word.lower())
        
    # Setup API keys
    api_manager = ApiKeyManager()
    print("\nWould you like to set up API keys now? They're optional but enable additional features.")
    setup_keys = input("Set up API keys? (y/n): ").lower() == 'y'
    
    if setup_keys:
        print("\nAPI keys will be encrypted. Please set an encryption password.")
        api_manager.setup_encryption()
        
        # Ask for common API keys
        services = [
            ("OPENWEATHER_API_KEY", "OpenWeather API (for weather forecasts)"),
            ("NEWS_API_KEY", "News API (for news updates)"),
            ("OPENAI_API_KEY", "OpenAI API (for advanced language processing)")
        ]
        
        for service_name, description in services:
            print(f"\n{description}")
            key = input(f"Enter API key for {service_name} (leave blank to skip): ").strip()
            if key:
                api_manager.set_api_key(service_name, key)
    
    print("\nSetup complete! You can run 'python main.py' to start your assistant.")

def main():
    """Main function to run the assistant"""
    # Setup environment
    setup_environment()
    
    # Parse arguments
    args = parse_arguments()
    
    # Run setup if requested
    if args.setup:
        run_setup()
        return
    
    # Initialize voice assistant
    assistant = VoiceAssistant()
    
    # Override preferences with command-line arguments
    if args.no_tts:
        assistant.preferences.set_preference("use_tts", False)
        assistant._setup_tts()
    
    if args.no_stt:
        assistant.preferences.set_preference("use_stt", False)
        assistant._setup_stt()
    
    # Run the assistant in the requested mode
    if args.console:
        assistant.run_console()
    else:
        print("Starting Natasha Voice Assistant...")
        assistant.start()
        
        # For now, just use console mode
        assistant.run_console()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAssistant terminated by user.")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
