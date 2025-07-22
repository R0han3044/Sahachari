import os
import io
import tempfile
import streamlit as st
from gtts import gTTS
import requests

class TTSService:
    """Text-to-Speech service using gTTS and fallback options"""
    
    def __init__(self):
        self.google_api_key = os.getenv("GOOGLE_CLOUD_TTS_API_KEY", None)
        self.use_google_api = self.google_api_key is not None
        
    def generate_audio(self, text, language='en', slow=False):
        """
        Generate audio from text
        
        Args:
            text (str): Text to convert to speech
            language (str): Language code ('en', 'te', etc.)
            slow (bool): Whether to speak slowly
            
        Returns:
            bytes: Audio file content or None if failed
        """
        if not text or not text.strip():
            return None
            
        try:
            # Use Google Cloud TTS API if available
            if self.use_google_api and language in ['en', 'te']:
                return self._generate_with_google_api(text, language, slow)
            else:
                # Use gTTS as fallback
                return self._generate_with_gtts(text, language, slow)
                
        except Exception as e:
            st.error(f"Audio generation failed: {str(e)}")
            return None
    
    def _generate_with_google_api(self, text, language, slow):
        """Generate audio using Google Cloud TTS API"""
        url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={self.google_api_key}"
        
        # Map language codes for Google API
        lang_map = {
            'en': 'en-US',
            'te': 'te-IN'
        }
        
        voice_map = {
            'en': {'languageCode': 'en-US', 'name': 'en-US-Standard-D'},
            'te': {'languageCode': 'te-IN', 'name': 'te-IN-Standard-A'}
        }
        
        data = {
            'input': {'text': text},
            'voice': voice_map.get(language, voice_map['en']),
            'audioConfig': {
                'audioEncoding': 'MP3',
                'speakingRate': 0.75 if slow else 1.0
            }
        }
        
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            import base64
            audio_content = base64.b64decode(result['audioContent'])
            return audio_content
        else:
            raise Exception(f"Google API request failed with status {response.status_code}")
    
    def _generate_with_gtts(self, text, language, slow):
        """Generate audio using gTTS"""
        # Map language codes for gTTS
        lang_map = {
            'te': 'te',  # Telugu
            'en': 'en',  # English
            'hi': 'hi',  # Hindi
            'ta': 'ta',  # Tamil
        }
        
        gtts_lang = lang_map.get(language, 'en')
        
        try:
            # Create gTTS object
            tts = gTTS(text=text, lang=gtts_lang, slow=slow)
            
            # Save to bytes buffer
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            
            return audio_buffer.getvalue()
            
        except Exception as e:
            # If Telugu is not supported, try English
            if language == 'te':
                st.warning("Telugu TTS not available, using English")
                tts = gTTS(text=text, lang='en', slow=slow)
                audio_buffer = io.BytesIO()
                tts.write_to_fp(audio_buffer)
                audio_buffer.seek(0)
                return audio_buffer.getvalue()
            else:
                raise e
    
    def get_supported_languages(self):
        """Get list of supported languages for TTS"""
        return {
            'en': 'English',
            'te': 'Telugu',
            'hi': 'Hindi',
            'ta': 'Tamil',
            'kn': 'Kannada',
            'ml': 'Malayalam'
        }
    
    def save_audio_file(self, audio_content, filename=None):
        """
        Save audio content to a temporary file
        
        Args:
            audio_content (bytes): Audio file content
            filename (str): Optional filename
            
        Returns:
            str: Path to saved file
        """
        if not filename:
            filename = f"tts_audio_{hash(audio_content)}.mp3"
        
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, filename)
        
        with open(file_path, 'wb') as f:
            f.write(audio_content)
        
        return file_path
    
    def validate_text_length(self, text, max_length=5000):
        """
        Validate text length for TTS processing
        
        Args:
            text (str): Text to validate
            max_length (int): Maximum allowed length
            
        Returns:
            bool: True if text is valid length
        """
        return len(text) <= max_length
    
    def chunk_text(self, text, chunk_size=4000):
        """
        Split long text into chunks for TTS processing
        
        Args:
            text (str): Text to chunk
            chunk_size (int): Maximum chunk size
            
        Returns:
            list: List of text chunks
        """
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        sentences = text.split('. ')
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk + sentence) <= chunk_size:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
