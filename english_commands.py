from spotify_actions import get_current_song, find_playlist_id, get_current_song_name
from validation import speak_validation 
from spotify_actions import get_current_song, find_playlist_id, get_current_song_name
from english_emojis import replace_emojis

def detect_command(text: str) -> str:
    text = text.lower()
    if "add" in text and "playlist" in text:
        return "add_to_playlist"
    elif "add" in text and "playlist" in text and "emoji" in text:
        return "add_to_playlist"
    elif "add" in text and "favorites" in text:
        return "add_to_favorites"
    elif "name" in text and "song" in text:
        return "say_song_name"
    elif "play" in text:
        return "play"
    elif "stop" in text:
        return "stop"
    elif "next" in text:
        return "next"
    elif "pre" in text:
        return "pre"
    return "unknown"

def process_commands_english(sp, text):
    if not isinstance(text, str) or text is None:
        print("Error: No valid text input provided")
        speak_validation("i didn't understand the command.")
        return None

    command = detect_command(text)

    match command:
        case "add_to_playlist":
            part = text.split("playlist")
            playlist_name = part[-1].strip()
            if "emoji" in playlist_name:
                playlist_name = replace_emojis(playlist_name)
            
            print(f"add to playlist: {playlist_name}")

            uri = get_current_song(sp)
            if uri is None:
                print("No songs playing.")
                speak_validation("No songs playing")
                return

            playlist_id = find_playlist_id(sp, playlist_name)
            if playlist_id is None:
                print(f"playlist not found: {playlist_name}")
                speak_validation(f"playlisy not found {playlist_name}. make sure it exists.")
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
                print(f"The song it's already exists in this playlist {playlist_name}.")
                speak_validation(f"The song it's already exists in this playlist {playlist_name}.")
                return
            
            sp.playlist_add_items(playlist_id, [uri])
            print(f"songs added to playlist {playlist_name} succsessfully.")
            speak_validation(f"songs added to playlist successfully")

        case "add_to_favorites":
            uri = get_current_song(sp)
            if uri is None:
                print("no song playing")
                speak_validation("no song playing")
                return
            sp.current_user_saved_tracks_add([uri])
            print("songs added to favorites.")
            speak_validation("songs added to favorites.")

        case "say_song_name":
            song_name = get_current_song_name(sp)
            if song_name is None:
                print("No song playing.")
                speak_validation("No song playing.")
                return
            print(f"current song is: {song_name}")
            speak_validation(f"current song is {song_name}")

        case "play":
            sp.start_playback()
            speak_validation("Playing song.")

        case "stop":
            sp.pause_playback()
            speak_validation("Pausing song.")
        case "next":
            sp.next_track()
            speak_validation("next song.")
        case "pre":
            sp.previous_track()
            speak_validation("previous song.")
        case _:
            print("unrecognized command.")
            speak_validation("i didn't understand that command.")


