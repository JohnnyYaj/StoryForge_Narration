import openai
import random
from google.cloud import texttospeech



# TODO:
# Find an API To make convert thr story to a audio file the push it to tiktok or youtube 
# Maybe make it faster?
# Find a Video editing API 

API_keys = open("API_KEY.txt",'r').read()
openai.api_key = API_keys # OpenAi API Key to access OpenAi chatbase 
stories_Genre = ["Science Fiction", "Fantasy","Mystery/Thriler","Romance","Historical Fiction","Adventure","Dystopian","Young Adult","Horror","Slice of Life"]
stories_made = []

# Picks 2 Random Genre
def get_RandomGenre():
    Genres = random.sample(stories_Genre,2)
    Genre1 = Genres[0]
    Genre2 = Genres[1]
        
    return "can you create a story involving these 2 genres " + Genre2 + " and "+Genre1 + "and remove the Chapter # and just continue it like usual"

# Makes a story genrated from 2 genres
def make_stories():
    stories_made.append({"role": "user", "content": get_RandomGenre()})
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = stories_made
    )
    return response['choices'][0]['message']['content']

def synthesize_text(text): # The Main TTS 
    client = texttospeech.TextToSpeechClient.from_service_account_file("key.json") # Google API KEY to access tts 

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(language_code="en-US-Polyglot-1", ssml_gender=texttospeech.SsmlVoiceGender.MALE) #Check this otherwise go back to te regular code 
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    
    rand_num = "".join([str(random.randint(0,5)) for x in range(5)]) # Creates a code so it is different from the others 
    output = f"output{rand_num}.mp3"
    
    with open(output, "wb") as out: # Makes the MP3 
        out.write(response.audio_content)  
        print(f'Audio content written to file "{output}"')


if __name__ == "__main__":  
    synthesize_text("Hello World")


