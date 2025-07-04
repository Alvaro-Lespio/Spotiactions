import speech_recognition as sr
from difflib import get_close_matches
from voice_response import speak_text

def listen_command():
    recognizer = sr.Recognizer()

    with sr.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic, duration=0.4)
        try:
            audio = recognizer.listen(mic)
            text = recognizer.recognize_google(audio, language="es-ES")
            text = text.lower()
            print(f"Estas son tus palabras --> {text}")
            return text
        except sr.UnknownValueError:
            print("No se entendió lo que dijiste. Intentá de nuevo.")
        except sr.RequestError as e:
            print(f"Error al conectarse a Google: {e}")
