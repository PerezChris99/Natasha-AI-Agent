import threading
import time

class SpeechRecognizer:
    """Handles speech recognition functionality"""
    
    def __init__(self, recognition_callback):
        self.recognition_callback = recognition_callback
        self.listening_thread = None
        self.is_listening = False
        
        # Try to import speech recognition library
        try:
            import speech_recognition as sr
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            self.sr_available = True
            
            # Adjust for ambient noise
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                
        except ImportError:
            print("Speech recognition library not available.")
            print("Please install it using: pip install SpeechRecognition PyAudio")
            self.sr_available = False

    def start_listening(self):
        """Start the listening thread"""
        if not self.sr_available:
            print("Speech recognition not available, only text input will work.")
            return
            
        if self.listening_thread is None or not self.listening_thread.is_alive():
            self.is_listening = True
            self.listening_thread = threading.Thread(target=self._listen_loop, daemon=True)
            self.listening_thread.start()

    def stop_listening(self):
        """Stop the listening thread"""
        self.is_listening = False
        if self.listening_thread and self.listening_thread.is_alive():
            self.listening_thread.join(timeout=1.0)

    def _listen_loop(self):
        """Continuously listen for speech"""
        import speech_recognition as sr
        
        while self.is_listening:
            try:
                with self.microphone as source:
                    print("Listening...")
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                
                try:
                    text = self.recognizer.recognize_google(audio)
                    print(f"Recognized: {text}")
                    
                    # Call the callback with recognized text
                    self.recognition_callback(text)
                    
                except sr.UnknownValueError:
                    print("Speech not recognized")
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")
                    
            except Exception as e:
                print(f"Error in speech recognition: {e}")
                time.sleep(1)  # Prevent rapid error loops
