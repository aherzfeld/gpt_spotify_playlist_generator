import openai
from dotenv import dotenv_values
import json


config = dotenv_values('.env')
openai.api_key = config['OPENAI_API_KEY']

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
     {'role': 'user', 'content': 'Generate a playlist of songs based on this prompt: haunting classical guitar'},
     {'role': 'assistant', 'content': example_json},
     {'role': 'user', 'content': 'Generate a playlist of songs based on this prompt: electro with strong bass'},

]

response = openai.ChatCompletion.create(
    messages=messages,
    model='gpt-3.5-turbo',
    max_tokens=400
)

# print(response['choices'][0]['message']['content'])

def get_playlist(prompt):
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
        {'role': 'user', 'content': 'Generate a playlist of songs based on this prompt: haunting classical guitar'},
        {'role': 'assistant', 'content': example_json},
        {'role': 'user', 'content': f'Generate a playlist of songs based on this prompt: {prompt}'},

    ]

    response = openai.ChatCompletion.create(
        messages=messages,
        model='gpt-3.5-turbo',
        max_tokens=400
    )

    playlist = json.loads((response['choices'][0]['message']['content']))
    print(playlist)