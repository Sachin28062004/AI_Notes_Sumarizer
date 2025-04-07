import speech_recognition as sr
from pydub import AudioSegment
import os
import tempfile
from typing import Optional

class SpeechToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()
    
    def convert_audio_to_wav(self, audio_path: str) -> Optional[str]:
        """Convert audio file to WAV format for processing."""
        try:
            # Create temp file for WAV output
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            temp_wav_path = temp_file.name
            temp_file.close()
            
            # Get file extension
            _, file_extension = os.path.splitext(audio_path)
            file_extension = file_extension.lower()
            
            # Convert based on file type
            if file_extension == '.mp3':
                sound = AudioSegment.from_mp3(audio_path)
            elif file_extension == '.wav':
                return audio_path  # Already WAV format
            elif file_extension == '.ogg':
                sound = AudioSegment.from_ogg(audio_path)
            elif file_extension in ['.m4a', '.mp4']:
                sound = AudioSegment.from_file(audio_path, format='m4a')
            else:
                print(f"Unsupported audio format: {file_extension}")
                return None
                
            # Export as WAV
            sound.export(temp_wav_path, format="wav")
            return temp_wav_path
            
        except Exception as e:
            print(f"Error converting audio: {e}")
            return None
    
    def process_audio(self, audio_path: str) -> str:
        """Process audio file and convert speech to text."""
        try:
            # Convert to WAV if needed
            wav_path = self.convert_audio_to_wav(audio_path)
            if not wav_path:
                return "Error processing audio file."
            
            # Process WAV file
            with sr.AudioFile(wav_path) as source:
                audio_data = self.recognizer.record(source)
                
                # Use Google's speech recognition
                text = self.recognizer.recognize_google(audio_data)
                
                # Clean up temp file if we created one
                if wav_path != audio_path:
                    os.unlink(wav_path)
                    
                return text
                
        except sr.UnknownValueError:
            return "Speech recognition could not understand the audio."
        except sr.RequestError as e:
            return f"Could not request results from speech recognition service: {e}"
        except Exception as e:
            print(f"Error processing audio: {e}")
            return "Error processing audio file."