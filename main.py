import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
from settings import get_language,set_language,set_audio_bot,load_config
from pynput import keyboard
from voice_listener import listen_command
from spanish_commands import process_commands
from english_commands import process_commands_english
from validation import speak_validation
load_dotenv()
#for this app, need you play at least one song. With this, the app recognize a device activate.

should_exit =False
pending_config=False
should_run_bot = False

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope=(
    "user-read-playback-state "
    "user-modify-playback-state "
    "playlist-read-private "
    "playlist-modify-public "
    "playlist-modify-private "
    "user-library-modify"
    ),
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    redirect_uri=os.getenv("REDIRECT_URI"),
    cache_path=".cache-user", 
))
user = sp.current_user()

def run_bot(sp):
    if get_language() == "EN":
        command = listen_command()
        print(f"Recognize text: {command}")
        process_commands_english(sp,command)
    else:    
        command = listen_command()
        print(f"Texto reconocido: {command}")
        process_commands(sp, command)

current_keys = {
    keyboard.Key.alt_l: False,
    keyboard.Key.alt_r: False,
    keyboard.Key.alt_gr: False
}


def on_press(key):
    global should_exit, pending_config,should_run_bot


    if key in current_keys:
        current_keys[key] = True
   
    if key == keyboard.KeyCode.from_char('c') and any(current_keys.values()):
        should_run_bot = True
        return False

    elif key == keyboard.KeyCode.from_char('q') and any(current_keys.values()):
        print("Atajo Alt+Q detectado, saliendo...")
        should_exit = True
        return False 
    
    elif key == keyboard.KeyCode.from_char('d') and any(current_keys.values()):
        pending_config = True
        return False 
    
def on_release(key):
    if key in current_keys:
        current_keys[key] = False

def init_bot():
    with keyboard.Listener(
        on_press=on_press,
        on_release=on_release
    ) as listener:
        if get_language() == "ES":
            print("Bot activo")
            print("Alt + C → Activar escucha de voz")
            print("Alt + Q → Cerrar el bot")
            print("Alt + D -> Configuración")
            listener.join()
        else:
            print("Active bot")
            print("Alt + C -> Activate listener")
            print("Alt + Q -> Close bot")
            print("Alt + D -> Settings")
            listener.join()

def show_config_menu():
    if get_language() == "ES":

        new_language = input("CAMBIAR LENGUAJE (ES/EN): ").strip().upper()
        while new_language not in ["ES", "EN"]:
            new_language = input("INTENTE NUEVAMENTE (ES/EN): ").strip().upper()
        set_language(new_language)

        new_audio_bot = input("ACTIVAR BOT DE AUDIO? (yes/no): ").strip().lower()
        while new_audio_bot not in ["yes", "no"]:
            new_audio_bot = input("INTENTE NUEVAMENTE (yes/no): ").strip().lower()

        set_audio_bot(new_audio_bot == "yes")
        print("CONFIGURACION ACTUALIZADA")
        input("PRESIONE ENTER PARA ENTRAR AL MENU...")
    else:
        new_language = input("SET LANGUAGE (ES/EN): ").strip().upper()
        while new_language not in ["ES", "EN"]:
            new_language = input("TRY AGAIN(ES/EN): ").strip().upper()
        set_language(new_language)

        new_audio_bot = input("ENABLE AUDIO BOT? (yes/no): ").strip().lower()
        while new_audio_bot not in ["yes", "no"]:
            new_audio_bot = input("TRY AGAIN (yes/no): ").strip().lower()

        set_audio_bot(new_audio_bot == "yes")
        print("CONFIGURATION UPDATED")
        input("PRESS ETNER TO RETURN TO MENU...")



while True:
    init_bot()  

    if should_exit:
        break

    if pending_config:
        show_config_menu()
        pending_config = False
        continue  

    if should_run_bot:
        try:
            run_bot(sp)
        except Exception as e:
            print("❌ Ocurrió un error dentro de run_bot:", e)
            speak_validation("Ocurrió un error, pero sigo funcionando.")
        should_run_bot = False
