from settings import get_audio_bot
from voice_response import speak_text

def speak_validation(text):
    if get_audio_bot() == True:
        speak_text(text)
