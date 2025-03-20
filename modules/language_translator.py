import requests
import json
import os
from googletrans import Translator as GoogleTranslator

class LanguageTranslator:
    """Language translation service"""
    
    def __init__(self, api_key_manager=None):
        """Initialize language translator"""
        self.api_key_manager = api_key_manager
        
        # Initialize Google Translate as fallback
        try:
            self.google_translator = GoogleTranslator()
            self.google_available = True
        except:
            self.google_available = False
            print("Google Translator not available")
    
    def detect_language(self, text):
        """Detect language of text"""
        if not text:
            return "en"  # Default to English
            
        # Try using Google Translate
        if self.google_available:
            try:
                detection = self.google_translator.detect(text)
                return detection.lang
            except Exception as e:
                print(f"Google language detection error: {e}")
        
        # Azure Cognitive Services as an alternative
        if self.api_key_manager and self.api_key_manager.get_api_key("azure_translator"):
            try:
                subscription_key = self.api_key_manager.get_api_key("azure_translator")
                endpoint = "https://api.cognitive.microsofttranslator.com/detect"
                
                headers = {
                    'Ocp-Apim-Subscription-Key': subscription_key,
                    'Ocp-Apim-Subscription-Region': 'global',
                    'Content-Type': 'application/json'
                }
                
                body = [{
                    'text': text[:100]  # Limit text size
                }]
                
                response = requests.post(endpoint, headers=headers, json=body)
                response.raise_for_status()
                
                result = response.json()
                return result[0]['language']
            except Exception as e:
                print(f"Azure language detection error: {e}")
        
        # Default fallback
        return "en"
    
    def translate(self, text, target_language="en", source_language=None):
        """Translate text to target language"""
        if not text:
            return text
            
        if not source_language:
            source_language = self.detect_language(text)
            
        # No need to translate if already in target language
        if source_language == target_language:
            return text
        
        # Try Google Translate first (no API key needed)
        if self.google_available:
            try:
                result = self.google_translator.translate(
                    text, dest=target_language, src=source_language)
                return result.text
            except Exception as e:
                print(f"Google translation error: {e}")
        
        # Azure Cognitive Services as an alternative
        if self.api_key_manager and self.api_key_manager.get_api_key("azure_translator"):
            try:
                subscription_key = self.api_key_manager.get_api_key("azure_translator")
                endpoint = "https://api.cognitive.microsofttranslator.com/translate"
                
                headers = {
                    'Ocp-Apim-Subscription-Key': subscription_key,
                    'Ocp-Apim-Subscription-Region': 'global',
                    'Content-Type': 'application/json'
                }
                
                params = {
                    'api-version': '3.0',
                    'from': source_language,
                    'to': target_language
                }
                
                body = [{
                    'text': text
                }]
                
                response = requests.post(endpoint, headers=headers, params=params, json=body)
                response.raise_for_status()
                
                result = response.json()
                return result[0]['translations'][0]['text']
            except Exception as e:
                print(f"Azure translation error: {e}")
        
        # If all else fails, return the original text
        print("No translation service available, returning original text")
        return text
    
    def get_supported_languages(self):
        """Get list of supported languages"""
        languages = {
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese",
            "nl": "Dutch",
            "ru": "Russian",
            "zh": "Chinese",
            "ja": "Japanese",
            "ko": "Korean",
            "ar": "Arabic",
            "hi": "Hindi"
        }
        
        return languages
