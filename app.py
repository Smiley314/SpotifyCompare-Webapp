from flask import Flask, render_template, request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)

playlists1 = []
playlists2 = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username1 = request.form['username1']
        username2 = request.form['username2']
        return display_playlists(username1, username2)
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    # Get the entered playlist IDs from the form data
    playlist1_id = request.form['playlist1']
    playlist2_id = request.form['playlist2']

    # Check if the entered playlist IDs are valid

    # Run your comparison function or perform any other desired processing
    common_tracks = compare_playlists(playlist1_id, playlist2_id)

    playlist_name_first = get_playlist_name_by_id(playlist1_id, playlists1)
    playlist_name_two = get_playlist_name_by_id(playlist2_id, playlists2)

    # Pass the playlists and common tracks to the results.html template
    return render_template('result.html', playlist1=playlist_name_first, playlist2=playlist_name_two, common_tracks=common_tracks)
    """"
    if playlist1_id in playlists1 and playlist2_id in playlists2:
        # Retrieve the corresponding playlists based on the playlist IDs
        playlist1_name = playlists1[playlist1_id]
        playlist2_name = playlists2[playlist2_id]

        # Run your comparison function or perform any other desired processing
        common_tracks = compare_playlists(playlist1_id, playlist2_id)

        # Pass the playlists and common tracks to the results.html template
        return render_template('result.html', playlist1=playlist1_name, playlist2=playlist2_name, common_tracks=common_tracks)
    else:
        # Handle the case when invalid playlist IDs are entered
        error_message = "Invalid playlist IDs."
        return render_template('error.html', error_message=error_message)
    """
def compare_playlists(playlist1_id, playlist2_id):
    # Set up your client_id and client_secret
    client_id = 'd148768cc9cd4b96af6cc68c20cd2a45'
    client_secret = 'a4981a3376d3475a98900869897fff58'

    # Authenticate with the Spotify API
    credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=credentials_manager)

    # Retrieve the tracks of playlist1
    playlist1_tracks = sp.playlist_tracks(playlist1_id)['items']
    playlist1_track_names = [track['track']['name'] for track in playlist1_tracks]

    # Retrieve the tracks of playlist2
    playlist2_tracks = sp.playlist_tracks(playlist2_id)['items']
    playlist2_track_names = [track['track']['name'] for track in playlist2_tracks]

    # Find the common tracks between the two playlists
    common_tracks = list(set(playlist1_track_names) & set(playlist2_track_names))

    return common_tracks

def get_playlist_name_by_id(playlist_id, playlist_target):
    for playlist_tuple in playlist_target:
        if playlist_tuple[0] == playlist_id:
            return playlist_tuple[1]
    return None

def display_playlists(username1, username2):
    # Set up your client_id and client_secret
    client_id = 'd148768cc9cd4b96af6cc68c20cd2a45'
    client_secret = 'a4981a3376d3475a98900869897fff58'

    # Authenticate with the Spotify API
    credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=credentials_manager)

    # Clear the playlist lists before populating them
    playlists1.clear()
    playlists2.clear()

    # Access playlist details for user 1
    user1_playlists = sp.user_playlists(username1)

    # Extract playlist names and IDs for user 1
    for playlist in user1_playlists['items']:
        if not playlist['public']:
            continue  # Skip if playlist is not public
        playlist_name = playlist['name']
        playlist_id = playlist['id']
        playlists1.append((playlist_id, playlist_name))

    # Access playlist details for user 2
    user2_playlists = sp.user_playlists(username2)

    # Extract playlist names and IDs for user 2
    for playlist in user2_playlists['items']:
        if not playlist['public']:
            continue  # Skip if playlist is not public
        playlist_name = playlist['name']
        playlist_id = playlist['id']
        playlists2.append((playlist_id, playlist_name))

    return render_template('playlists.html', username1=username1, username2=username2, playlists1=playlists1, playlists2=playlists2)

if __name__ == '__main__':
    app.run(debug=True)
