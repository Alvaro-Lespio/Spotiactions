def get_current_song(sp):
    current_song = sp.current_playback()
    if current_song and current_song["is_playing"]:
        return current_song['item']['uri']
    return None

def find_playlist_id(sp,playlist_name):
    playlists = sp.current_user_playlists()
    for playlist in playlists['items']:
        print(f"Nombre encontrado: '{playlist['name']}'") 
        if playlist['name'].lower() == playlist_name.lower():
            return playlist['id']
    return None

def find_playlist_uri(sp,playlist_name):
    playlists = sp.current_user_playlists()
    for playlist in playlists['items']:
        if playlist['name'].lower() == playlist_name.lower():
            return playlist['uri']
    return None

def add_song_to_playlist(sp, song_uri, playlist_id):
    sp.playlist_add_items(playlist_id, [song_uri])

def get_current_song_name(sp):
    current_song = sp.current_playback()
    if current_song and current_song["is_playing"]:
        return current_song['item']['name']
    return None

def add_song_to_favorites(sp, song_uri):
    sp.current_user_saved_tracks_add([song_uri])
    print("Canción agregada a favoritos exitosamente.")
    