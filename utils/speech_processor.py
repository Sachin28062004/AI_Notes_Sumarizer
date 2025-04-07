import speech_recognition as sr

def process_audio(audio_path):
    """
    Convert speech in audio file to text.
    Supports formats compatible with SpeechRecognition library.
    """
    recognizer = sr.Recognizer()
    
    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            return text
    except Exception as e:
        return f"Error processing audio: {str(e)}"
