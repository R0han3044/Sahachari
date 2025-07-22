import os
import streamlit as st
from googletrans import Translator
import requests
import json

class TranslationService:
    """Translation service using Google Translate or fallback APIs"""
    
    def __init__(self):
        self.translator = Translator()
        self.api_key = os.getenv("GOOGLE_TRANSLATE_API_KEY", None)
        self.use_api = self.api_key is not None
        
    def translate_text(self, text, target_language):
        """
        Translate text to target language
        
        Args:
            text (str): Text to translate
            target_language (str): Target language code ('en' or 'te')
            
        Returns:
            str: Translated text
        """
        if not text or not text.strip():
            return ""
            
        try:
            # Use Google Translate API if available
            if self.use_api:
                return self._translate_with_api(text, target_language)
            else:
                # Use googletrans library as fallback
                return self._translate_with_library(text, target_language)
                
        except Exception as e:
            st.error(f"Translation error: {str(e)}")
            return text  # Return original text if translation fails
    
    def _translate_with_api(self, text, target_language):
        """Translate using Google Translate API"""
        url = "https://translation.googleapis.com/language/translate/v2"
        
        params = {
            'key': self.api_key,
            'q': text,
            'target': target_language,
            'format': 'text'
        }
        
        response = requests.post(url, data=params)
        
        if response.status_code == 200:
            result = response.json()
            return result['data']['translations'][0]['translatedText']
        else:
            raise Exception(f"API request failed with status {response.status_code}")
    
    def _translate_with_library(self, text, target_language):
        """Translate using googletrans library"""
        try:
            result = self.translator.translate(text, dest=target_language)
            return result.text
        except Exception as e:
            # If googletrans fails, try alternative approach
            raise Exception(f"Library translation failed: {str(e)}")
    
    def detect_language(self, text):
        """
        Detect the language of given text
        
        Args:
            text (str): Text to analyze
            
        Returns:
            str: Detected language code
        """
        try:
            if self.use_api:
                return self._detect_with_api(text)
            else:
                return self._detect_with_library(text)
        except Exception as e:
            st.warning(f"Language detection failed: {str(e)}")
            return 'en'  # Default to English
    
    def _detect_with_api(self, text):
        """Detect language using Google Translate API"""
        url = "https://translation.googleapis.com/language/translate/v2/detect"
        
        params = {
            'key': self.api_key,
            'q': text
        }
        
        response = requests.post(url, data=params)
        
        if response.status_code == 200:
            result = response.json()
            return result['data']['detections'][0][0]['language']
        else:
            raise Exception(f"API request failed with status {response.status_code}")
    
    def _detect_with_library(self, text):
        """Detect language using googletrans library"""
        result = self.translator.detect(text)
        return result.lang
    
    def get_supported_languages(self):
        """Get list of supported languages"""
        return {
            'en': 'English',
            'te': 'Telugu',
            'hi': 'Hindi',
            'ta': 'Tamil',
            'kn': 'Kannada',
            'ml': 'Malayalam'
        }
    
    def batch_translate(self, texts, target_language):
        """
        Translate multiple texts at once
        
        Args:
            texts (list): List of texts to translate
            target_language (str): Target language code
            
        Returns:
            list: List of translated texts
        """
        translated_texts = []
        
        for text in texts:
            try:
                translated = self.translate_text(text, target_language)
                translated_texts.append(translated)
            except Exception as e:
                st.warning(f"Failed to translate text: {text[:50]}...")
                translated_texts.append(text)  # Keep original if translation fails
        
        return translated_texts
