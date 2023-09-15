import openai
import random

# TODO:
# Find an API To make convert thr story to a audio file the push it to tiktok 
# Maybe make it faster?

# import requests

# url = "https://play.ht/api/v1/convert"

# headers = {
#     "accept": "audio/mpeg",
#     "content-type": "application/json",
#     "AUTHORIZATION": "edd0cb5664864461b143294c2ba15867",
#     "X-USER-ID": "UMTlb9AGVzVpqfeB7U75V11o2903"
# }

API_keys = open("API_KEY.txt",'r').read()
openai.api_key = API_keys
stories_Genre = ["Science Fiction", "Fantasy","Mystery/Thriler","Romance","Historical Fiction","Adventure","Dystopian","Young Adult","Horror","Slice of Life"]
stories_made = []


# Picks 2 Random Genre
def get_RandomGenre():
    Genres = random.sample(stories_Genre,2)
    Genre1 = Genres[0]
    Genre2 = Genres[1]
        
    return "can you create a story involving these 2 genres " + Genre2 + " and "+Genre1

# Makes a story genrated from 2 genres
def make_stories():
    stories_made.append({"role": "user", "content": get_RandomGenre()})
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = stories_made
    )
    return response['choices'][0]['message']['content']
    
    
# payload = {
#     "content": [make_stories()],
#     "voice": "Matthew"
# }
    
# response = requests.post(url, json=payload, headers=headers)
# print(response.text)