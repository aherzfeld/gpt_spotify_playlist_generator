import openai
from dotenv import dotenv_values
import json
import spotipy
import argparse

config = dotenv_values('.env')
openai.api_key = config['OPENAI_API_KEY']

parser = argparse.ArgumentParser(description='Simple command line song utility')
parser.add_argument('-p', type=str, help='The prompt to describe the playlist')
parser.add_argument('-n', type=str, default=8, help='The number of songs to add to the playlist')


args = parser.parse_args()


def get_playlist(prompt, count=8):
    example_json = """
    [
        {"song": "Asturias (Leyenda)", "artist": "Isaac Albeniz"},
        {"song": "Recuerdos de la Alhambra", "artist": "Francisco Tárrega"},
        {"song": "Capricho Arabe", "artist": "Francisco Tárrega"},
        {"song": "Sevilla", "artist": "Isaac Albeniz"},
        {"song": "Romanza", "artist": "Andrea De Segovia"}
    ]
    """

    messages = [
        {'role': 'system', 'content': """You are a helpful playlist assistant. 
        You should generate a list of songs and their artists according to a text prompt.
        You should return a json array, where each element follows this format: {"song": <song_title>, "artist": <artist_name>}"""
        },
        {'role': 'user', 'content': 'Generate a playlist of 5 songs based on this prompt: haunting classical guitar'},
        {'role': 'assistant', 'content': example_json},
        {'role': 'user', 'content': f'Generate a playlist of {count} songs based on this prompt: {prompt}'},

    ]

    response = openai.ChatCompletion.create(
        messages=messages,
        model='gpt-3.5-turbo',
        max_tokens=400
    )

    playlist = json.loads((response['choices'][0]['message']['content']))
    return playlist

playlist = get_playlist(args.p, args.n)
print(playlist)

sp = spotipy.Spotify(
    auth_manager=spotipy.SpotifyOAuth(
        client_id=config['SPOTIFY_CLIENT_ID'],
        client_secret=config['SPOTIFY_CLIENT_SECRET'],
        redirect_uri="http://localhost:9999",
        scope='playlist-modify-private'
    )
)

current_user = sp.current_user()

track_ids = []
assert current_user is not None

for item in playlist:
    artist, song = item['artist'], item['song']
    query = f'{song} {artist}'
    search_results = sp.search(q=query, type='track', limit=10)
    track_ids.append(search_results['tracks']['items'][0]['id'])

created_playlist = sp.user_playlist_create(
    current_user['id'],
    public=False,
    name='test playlist yay'
)

sp.user_playlist_add_tracks(current_user['id'], created_playlist['id'], track_ids)




