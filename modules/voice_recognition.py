import speech_recognition as sr
import pyttsx3
import os
import time
import numpy as np

class VoiceRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        
        # Configure speech engine
        voices = self.engine.getProperty('voices')
        # Try to set a female voice if available
        for voice in voices:
            if "female" in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
                
        # Set speech rate and volume
        self.engine.setProperty('rate', 175)  # Default is 200
        self.engine.setProperty('volume', 0.9)  # Default is 1.0
        
        # Energy threshold for wake word detection - adjust based on environment
        self.recognizer.energy_threshold = 300  # Default is 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.dynamic_energy_adjustment_damping = 0.15
        self.recognizer.dynamic_energy_ratio = 1.5
        
        # Wake words/phrases
        self.wake_words = ["natasha", "hey natasha", "ok natasha", "hi natasha"]
        
        # Microphone selection
        self.microphone = self._get_best_microphone()
        
    def _get_best_microphone(self):
        """Find the best microphone device or use default"""
        try:
            # List available microphones
            mics = sr.Microphone.list_microphone_names()
            print(f"Available microphones: {mics}")
            
            # Try to find preferred microphones - customize for your setup
            preferred_mics = ["array", "headset", "studio"]
            selected_mic = None
            
            for i, mic in enumerate(mics):
                for preferred in preferred_mics:
                    if preferred.lower() in mic.lower():
                        print(f"Selected preferred microphone: {mic}")
                        return sr.Microphone(device_index=i)
            
            # Default to system default microphone
            return sr.Microphone()
        except Exception as e:
            print(f"Error selecting microphone: {str(e)}")
            return sr.Microphone()
    
    def listen_for_wake_word(self):
        """Listen specifically for wake words with lower threshold"""
        with self.microphone as source:
            # Use a shorter timeout for wake word detection
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                print("Listening for wake word...")
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                try:
                    text = self.recognizer.recognize_google(audio).lower()
                    print(f"Heard: {text}")
                    # Check if any wake word is in the detected text
                    for wake_word in self.wake_words:
                        if wake_word in text:
                            return True
                except:
                    pass  # Ignore errors in wake word detection
            except:
                pass  # Timeout or other error
        return False

    def listen(self):
        """Listen for a command with noise reduction"""
        with self.microphone as source:
            print("Listening...")
            # Dynamically adjust for ambient noise
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                print("Processing speech...")
                
                # Try multiple recognition services for better accuracy
                try:
                    # First try Google (most reliable but requires internet)
                    text = self.recognizer.recognize_google(audio)
                    print(f"You said (Google): {text}")
                    return text.lower()
                except:
                    try:
                        # Fallback to Sphinx (offline, less accurate)
                        text = self.recognizer.recognize_sphinx(audio)
                        print(f"You said (Sphinx): {text}")
                        return text.lower()
                    except:
                        self.speak("Sorry, I didn't catch that")
                        return None
            except sr.WaitTimeoutError:
                print("Listening timed out")
                return None
            except Exception as e:
                print(f"Error in speech recognition: {str(e)}")
                return None

    def speak(self, text):
        """Convert text to speech with improved formatting"""
        if not text:
            return
            
        # Clean up the text for better speech
        text = text.replace('_', ' ').replace('-', ' ')
        
        # Break down long sentences
        sentences = text.split('. ')
        
        print(f"Assistant: {text}")
        
        for sentence in sentences:
            if sentence:
                self.engine.say(sentence)
                self.engine.runAndWait()
                # Brief pause between sentences for more natural speech
                time.sleep(0.1)
