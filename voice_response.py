import pyttsx3
import os
import uuid
from gtts import gTTS
from pygame import mixer
import time

def speak_text(text, lang="es"):
    try:
        # Crear TTS con idioma español
        tts = gTTS(text=text, lang=lang)

        # Crear archivo temporal único
        filename = f"/tmp/voice_{uuid.uuid4()}.mp3"
        tts.save(filename)

        # Reproducir el audio con pygame
        mixer.init()
        mixer.music.load(filename)
        mixer.music.play()

        # Esperar hasta que termine de reproducir
        while mixer.music.get_busy():
            time.sleep(0.1)

        # Borrar el archivo después
        os.remove(filename)

    except Exception as e:
        print("Error al reproducir el texto:", e)


