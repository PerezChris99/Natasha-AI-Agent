import pyttsx3

def speak(text):
    # Initialize the TTS engine
    engine = pyttsx3.init()
    
    # Set properties for voice (optional)
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 1)  # Volume (0.0 to 1.0)

    # Speak the text
    engine.say(text)
    engine.runAndWait()
