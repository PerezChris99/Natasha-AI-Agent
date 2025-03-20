from dotenv import load_dotenv
import os
from modules.voice_recognition import VoiceRecognizer
from modules.command_processor import CommandProcessor
from modules.spotify_controller import SpotifyController
from modules.youtube_controller import YouTubeController
from modules.app_manager import ApplicationManager
from flask import Flask, render_template
from utils.logger import ChatLogger
from modules.weather_service import WeatherService
from modules.news_service import NewsService
from modules.reminder_service import ReminderService
from modules.smart_home import SmartHomeController
from modules.calendar_service import CalendarService
from modules.fun_features import FunFeatures

load_dotenv()

class Natasha:
    def __init__(self):
        self.voice_recognizer = VoiceRecognizer()
        self.command_processor = CommandProcessor()
        self.spotify = SpotifyController()
        self.youtube = YouTubeController()
        self.app_manager = ApplicationManager()
        self.logger = ChatLogger()
        self.weather = WeatherService()
        self.news = NewsService()
        self.reminder = ReminderService(self.voice_recognizer)
        self.smart_home = SmartHomeController()
        self.calendar = CalendarService()
        self.fun = FunFeatures()
        
    def process_voice_command(self):
        command = self.voice_recognizer.listen()
        if command:
            result = self.command_processor.process(command)
            response = None
            
            if isinstance(result, tuple):
                command_type, data = result
                if command_type == 'weather':
                    response = self.weather.get_weather(data)
                elif command_type == 'news':
                    response = self.news.get_news_brief(data)
                elif command_type == 'timer':
                    response = self.reminder.set_timer(data)
                elif command_type == 'reminder':
                    message, hours = data
                    response = self.reminder.set_reminder(message, hours)
                elif command_type == 'smart_home':
                    device_name, action = data
                    response = self.smart_home.control_device(device_name, action)
                elif command_type == 'calendar':
                    response = self.calendar.get_events(data)
                elif command_type == 'joke':
                    response = self.fun.tell_joke()
                elif command_type == 'math':
                    response = self.fun.solve_math(data)
                elif command_type == 'coin':
                    response = self.fun.flip_coin()
                elif command_type == 'dice':
                    response = self.fun.roll_dice(data)

            self.logger.log_interaction(command, response)
            return response
        return None

    def run(self):
        print("Natasha is listening... Say something!")
        while True:
            self.process_voice_command()

if __name__ == "__main__":
    assistant = Natasha()
    assistant.run()
