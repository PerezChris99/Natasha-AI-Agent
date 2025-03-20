import os
import threading

class TextToSpeech:
    """Handles text-to-speech capabilities"""
    
    def __init__(self):
        # Try to import pyttsx3 for offline TTS
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)  # Speed
            self.engine.setProperty('volume', 0.8)  # Volume
            self.tts_available = True
            
            # Try to set a female voice if available
            voices = self.engine.getProperty('voices')
            for voice in voices:
                if 'female' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
        except ImportError:
            print("Text-to-speech library not available.")
            print("Please install it using: pip install pyttsx3")
            self.tts_available = False
        
        self.speaking = False
        self.speak_thread = None

    def speak(self, text):
        """Speak the given text"""
        if not text or not self.tts_available:
            return
            
        # Create a new thread for speaking to avoid blocking
        self.speaking = True
        if self.speak_thread and self.speak_thread.is_alive():
            self.stop()
            
        self.speak_thread = threading.Thread(target=self._speak_thread, args=(text,))
        self.speak_thread.start()

    def _speak_thread(self, text):
        """Thread function for speaking"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error in text-to-speech: {e}")
        finally:
            self.speaking = False

    def stop(self):
        """Stop current speech"""
        if self.tts_available and self.speaking:
            try:
                self.engine.stop()
            except:
                pass
            self.speaking = False
