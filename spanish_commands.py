from spotify_actions import get_current_song, find_playlist_id, get_current_song_name,find_playlist_uri
from validation import speak_validation
from spanish_emojis import replace_emojis
from voice_response import speak_text
import re
def detect_command(text: str) -> str:
    
    text = text.lower()
    if "agregar" in text and "playlist" in text:
        return "add_to_playlist"
    elif "agregar" in text and "playlist" in text and "emoji" in text:
        return "add_to_playlist"
    elif "agregar" in text and "favoritos" in text:
        return "add_to_favorites"
    elif "decime" in text or "nombre" in text and "canción" in text:
        return "say_song_name"
    elif "reproducir" in text and "playlist" in text:
        return"play_playlist"
    elif "reproducir" in text:
        return "play"
    elif "pausar" in text:
        return "pause"
    elif "siguiente" in text:
        return "next"
    elif "anterior" in text:
        return "previous"
    return "unknown"

def clean_song_name(name):
    return re.sub(r'[^\w\sáéíóúÁÉÍÓÚñÑ]', '', name)

def process_commands(sp, text):
    if not isinstance(text, str) or text is None:
        print("Error: No valid text input provided")
        speak_validation("No entendí el comando.")
        return None

    command = detect_command(text)

    match command:
        case "add_to_playlist":
            part = text.split("playlist")
            playlist_name = part[-1].strip()
            if "emoji" in playlist_name:
                playlist_name = replace_emojis(playlist_name)
            
            print(f"Agregando a la playlist: {playlist_name}")

            uri = get_current_song(sp)
            if uri is None:
                print("No hay canción actual para agregar a la playlist.")
                speak_validation("No estás escuchando ninguna canción.")
                return

            playlist_id = find_playlist_id(sp, playlist_name)
            if playlist_id is None:
                print(f"No se encontró la playlist: {playlist_name}")
                speak_validation(f"No se encontró la playlist {playlist_name}. Asegúrate de que exista.")
                return
            
            existing_tracks = []
            results = sp.playlist_items(playlist_id)
            while results:
                existing_tracks.extend([item["track"]["uri"] for item in results["items"]])
                if results.get("next"):
                    results = sp.next(results)
                else:
                    break

            if uri in existing_tracks:
                print(f"La canción ya está en la playlist {playlist_name}.")
                speak_validation(f"La canción ya está en la playlist {playlist_name}.")
                return
    
            sp.playlist_add_items(playlist_id, [uri])
            print(f"Canción agregada a la playlist {playlist_name} exitosamente.")
            speak_validation(f"Canción agregada a la playlist {playlist_name}")

        case "add_to_favorites":
            uri = get_current_song(sp)
            if uri is None:
                print("No hay canción actual para agregar a favoritos.")
                speak_validation("No estás escuchando ninguna canción.")
                return
            sp.current_user_saved_tracks_add([uri])
            print("Canción agregada a favoritos exitosamente.")
            speak_validation("Canción agregada a favoritos exitosamente.")

        case "say_song_name":
            song_name = get_current_song_name(sp)
            if song_name is None:
                print("No hay canción actual para identificar.")
                speak_validation("No estás escuchando ninguna canción.")
                return
            song_name_clean = clean_song_name(song_name)
            print(f"Nombre de la canción actual: {song_name}")
            speak_validation(f"La canción actual es {song_name_clean}")

        case "play":
            sp.start_playback()
            speak_validation("Reproduciendo canción.")

        case "pause":
            sp.pause_playback()
            speak_validation("Pausando canción.")
        case "play_playlist":
            part = text.split("playlist")
            playlist_name = part[-1].strip()
            print(f"playlist name {playlist_name}")
            playlist_id = find_playlist_id(sp, playlist_name)

            if playlist_id:
                sp.start_playback(context_uri=f"spotify:playlist:{playlist_id}")
                speak_validation(f"Reproduciendo la playlist {playlist_name}")     
            else:
                print("Playlist no encontrada.")
                speak_validation("No se encontró la playlist.")
            return
        case "next":
            sp.next_track()
            speak_validation("cancion siguiente.")
        case "previous":
            sp.previous_track()
            speak_validation("cancion anterior.")
        case _:
            print("Comando no reconocido.")
            speak_validation("No entendí ese comando.")



