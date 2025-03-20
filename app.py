try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv is not installed. Environment variables need to be set manually.")
    print("Please run: pip install -r requirements.txt")
    # Create a dummy function to prevent errors
    def load_dotenv():
        pass

import os
import time
import threading

# Check for other required modules
try:
    from modules.voice_recognition import VoiceRecognizer
    from modules.command_processor import CommandProcessor
    from modules.spotify_controller import SpotifyController
    from modules.youtube_controller import YouTubeController
    from modules.app_manager import ApplicationManager
    from modules.weather_service import WeatherService
    from modules.news_service import NewsService
    from modules.reminder_service import ReminderService
    from modules.smart_home import SmartHomeController
    from modules.calendar_service import CalendarService
    from modules.fun_features import FunFeatures
    from modules.volume_controller import VolumeController
    from modules.task_automation import TaskAutomation
    from modules.system_monitor import SystemMonitor
    from modules.security_system import SecuritySystem
    from modules.data_analyzer import DataAnalyzer
    from modules.context_manager import ContextManager
    from modules.ai_brain import AIBrain
    from utils.logger import ChatLogger
    from utils.settings import Settings
    from utils.error_handler import ErrorHandler
except ImportError as e:
    print(f"Error: Missing module - {str(e)}")
    print("Please run: pip install -r requirements.txt")
    exit(1)

class Natasha:
    def __init__(self):
        # Initialize settings and error handling first
        self.settings = Settings()
        self.error_handler = ErrorHandler()
        self.logger = ChatLogger()
        
        # Core components
        self.voice_recognizer = VoiceRecognizer()
        self.ai_brain = AIBrain()
        self.context_manager = ContextManager()
        
        # Command processing
        self.command_processor = CommandProcessor()
        
        # Service modules
        try:
            self.spotify = SpotifyController()
        except Exception as e:
            self.logger.log_error("Failed to initialize Spotify controller", str(e))
            self.spotify = None
            
        self.youtube = YouTubeController()
        self.app_manager = ApplicationManager()
        self.weather = WeatherService()
        self.news = NewsService()
        self.reminder = ReminderService(self.voice_recognizer)
        self.volume_controller = VolumeController()
        
        # Advanced features
        try:
            self.smart_home = SmartHomeController()
        except Exception as e:
            self.logger.log_error("Failed to initialize Smart Home controller", str(e))
            self.smart_home = None
            
        try:
            self.calendar = CalendarService()
        except Exception as e:
            self.logger.log_error("Failed to initialize Calendar service", str(e))
            self.calendar = None
            
        self.fun = FunFeatures()
        self.task_automation = TaskAutomation()
        self.system_monitor = SystemMonitor()
        
        try:
            self.security_system = SecuritySystem()
        except Exception as e:
            self.logger.log_error("Failed to initialize Security system", str(e))
            self.security_system = None
            
        self.data_analyzer = DataAnalyzer()
        
        # State variables
        self.listening = False
        self.last_context_update = time.time()
        self.last_command_time = time.time()
        self.conversation_context = ""
        
        # Start background services
        self._start_background_services()
        
    def _start_background_services(self):
        # Context update thread
        self.context_update_thread = threading.Thread(
            target=self._periodic_context_update, 
            daemon=True
        )
        self.context_update_thread.start()
        
        # System monitoring thread
        self.system_monitor_thread = threading.Thread(
            target=self._periodic_system_check, 
            daemon=True
        )
        self.system_monitor_thread.start()
        
    def _periodic_context_update(self):
        while True:
            try:
                # Update context every 10 minutes or when needed
                current_time = time.time()
                if current_time - self.last_context_update > 600:  # 10 minutes
                    self.context_manager.update_context()
                    self.last_context_update = current_time
            except Exception as e:
                self.logger.log_error("Context update error", str(e))
            time.sleep(60)  # Check every minute
            
    def _periodic_system_check(self):
        while True:
            try:
                # Check system health every 5 minutes
                system_status = self.system_monitor.get_system_status()
                if "CPU Usage" in system_status and "90%" in system_status:
                    self.voice_recognizer.speak("Warning: System resources are running low.")
            except Exception as e:
                self.logger.log_error("System monitoring error", str(e))
            time.sleep(300)  # Check every 5 minutes
        
    def start_listening(self):
        """Start actively listening for commands"""
        self.listening = True
        self.voice_recognizer.speak("I'm listening")
        
    def stop_listening(self):
        """Stop actively listening but remain in standby"""
        self.listening = False
        self.voice_recognizer.speak("Entering standby mode")
    
    def process_voice_command(self):
        if not self.listening:
            # In standby mode, only listen for wake word
            wake_word = self.voice_recognizer.listen_for_wake_word()
            if wake_word:
                self.start_listening()
                return "Listening activated"
            return None
        
        command = self.voice_recognizer.listen()
        if not command:
            return None
            
        self.last_command_time = time.time()
        
        try:
            # Update conversation context
            self.conversation_context += f"\nUser: {command}"
            
            # First try AI brain for natural language understanding
            sentiment, _ = self.ai_brain.analyze_sentiment(command)
            
            # Process the command
            result = self.command_processor.process(command)
            response = self._handle_command_result(result, command)
            
            if not response:
                # If no specific command matched, use AI to generate response
                response = self.ai_brain.generate_response(command)
                
            # Update conversation context with response
            self.conversation_context += f"\nNatasha: {response}"
            
            # Log the interaction
            self.logger.log_interaction(command, response, sentiment)
            
            # Speak the response
            self.voice_recognizer.speak(response)
            
            return response
        except Exception as e:
            error_msg = f"Error processing command: {str(e)}"
            self.logger.log_error("Command processing error", error_msg)
            self.voice_recognizer.speak("I'm sorry, I encountered an error processing that request")
            return error_msg
            
    def _handle_command_result(self, result, original_command):
        """Process the structured command result from the command processor"""
        if isinstance(result, str):
            return result
            
        if not isinstance(result, tuple) or len(result) != 2:
            return None
            
        command_type, data = result
        
        # Music and media
        if command_type == 'spotify' and self.spotify:
            return self.spotify.play_song(data)
        elif command_type == 'youtube':
            return self.youtube.play_video(data)
            
        # System controls
        elif command_type == 'volume' and isinstance(data, int):
            return self.volume_controller.set_volume(data)
        elif command_type == 'volume' and data == 'mute':
            return self.volume_controller.mute()
        elif command_type == 'volume' and data == 'unmute':
            return self.volume_controller.unmute()
        elif command_type == 'app':
            return self.app_manager.open_application(data)
            
        # Information services
        elif command_type == 'weather':
            return self.weather.get_weather(data)
        elif command_type == 'news':
            return self.news.get_news_brief(data)
        elif command_type == 'calendar' and self.calendar:
            return self.calendar.get_events(data)
            
        # Reminders and scheduling
        elif command_type == 'timer':
            return self.reminder.set_timer(data)
        elif command_type == 'reminder':
            message, hours = data
            return self.reminder.set_reminder(message, hours)
        elif command_type == 'schedule':
            return self.task_automation.add_scheduled_task(**data)
            
        # Smart home
        elif command_type == 'smart_home' and self.smart_home:
            device_name, action = data
            return self.smart_home.control_device(device_name, action)
            
        # Fun features
        elif command_type == 'joke':
            return self.fun.tell_joke()
        elif command_type == 'math':
            return self.fun.solve_math(data)
        elif command_type == 'coin':
            return self.fun.flip_coin()
        elif command_type == 'dice':
            return self.fun.roll_dice(data)
            
        # Security and monitoring
        elif command_type == 'identify' and self.security_system:
            return self.security_system.identify_person()
        elif command_type == 'add_face' and self.security_system:
            return self.security_system.add_face(data)
        elif command_type == 'system_status':
            return self.system_monitor.get_system_status()
        elif command_type == 'network_status':
            return self.system_monitor.get_network_status()
        elif command_type == 'processes':
            processes = self.system_monitor.monitor_processes()
            return "Top processes:\n" + "\n".join([f"{p['name']}: CPU {p['cpu']}%" for p in processes])
            
        # AI and analysis
        elif command_type == 'analyze_data':
            return self.data_analyzer.analyze_data(data)
        elif command_type == 'analyze_text':
            return self.ai_brain.analyze_sentiment(data)[0]
        elif command_type == 'summarize':
            return self.ai_brain.summarize_text(data)
        elif command_type == 'learn_pattern':
            input_text, response = data
            self.ai_brain.learn_pattern(input_text, response)
            return f"I've learned to respond to '{input_text}'"
        elif command_type == 'learn_fact':
            self.ai_brain.learn_fact(data)
            return "Thank you for teaching me that"
        elif command_type == 'context':
            return f"Current context: {self.context_manager.get_appropriate_response_style()}"
            
        # Unknown command type
        return None

    def run(self):
        """Run the assistant in continuous mode"""
        self.voice_recognizer.speak("Natasha initialized and ready")
        print("Natasha is running. Say the wake word to activate.")
        
        try:
            while True:
                self.process_voice_command()
                
                # Auto-standby after 5 minutes of inactivity
                if self.listening and time.time() - self.last_command_time > 300:
                    self.stop_listening()
                    
                time.sleep(0.1)  # Prevent CPU hogging
        except KeyboardInterrupt:
            print("Shutting down Natasha...")
            self.voice_recognizer.speak("Shutting down")
        except Exception as e:
            self.logger.log_error("Critical error", str(e))
            print(f"Critical error: {str(e)}")
            self.voice_recognizer.speak("Critical error encountered. Shutting down.")

if __name__ == "__main__":
    try:
        print("Initializing Natasha Assistant...")
        print("If you encounter any module errors, run: pip install -r requirements.txt")
        assistant = Natasha()
        assistant.run()
    except Exception as e:
        print(f"Critical initialization error: {str(e)}")
        print("Please install required packages: pip install -r requirements.txt")
