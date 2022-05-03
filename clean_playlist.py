import spotipy
from spotipy.oauth2 import SpotifyOAuth

# imports for testing
from pprint import pprint
from timeit import default_timer as timer

def main():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-private"))

    user_id = sp.current_user()['id']

    # Get all of the information from the playlist that needs cleaned
    old_playlist_id = '5ifdmqV6vTsIEAckZB4Ccy'
    old_playlist = sp.user_playlist(user_id, old_playlist_id)
    playlist_size = old_playlist['tracks']['total']
    
    # Can only retrieve 100 tracks at once so have to make multiple requests
    # for playlists larger than 100
    old_tracks = []
    for i in range(playlist_size//100 + 1):
        old_tracks = [*old_tracks, *sp.playlist_items(old_playlist_id, fields="items(track(explicit,id,name))", offset=i*100)['items']]

    # Get the name to create the new playlist name
    old_playlist_name = old_playlist['name']

    # Check every track in the old playlist and add it if it's not explicit
    tracks_to_add = []
    add_counter = 0
    for track in old_tracks:
        if not track['track']['explicit']:
            tracks_to_add.append(track['track']['id'])   
            print(f"Added: {track['track']['name']}")
            add_counter += 1
        else:
            print(f"NOT ADDED: {track['track']['name']}")

    # Create new playlist and add tracks
    new_playlist_name = old_playlist_name + ' (Clean)'
    new_playlist_id = sp.user_playlist_create(user_id, new_playlist_name, public=False)['id']
    sp.user_playlist_add_tracks(user_id, new_playlist_id, tracks_to_add)
    print(f"Added {add_counter} tracks")

if __name__ == "__main__":
    start = timer()
    main()
    end = timer()
    print(end - start)