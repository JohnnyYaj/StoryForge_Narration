import openai
import random
from google.cloud import texttospeech
from moviepy.editor import VideoFileClip, vfx ,AudioFileClip, afx, CompositeAudioClip, concatenate_videoclips
from mutagen.mp3 import MP3
import os

# TODO:
# Clean it up 
# Miore Themes
# Have Fun

API_keys = open("API_KEY.txt",'r').read()
openai.api_key = API_keys # OpenAi API Key to access OpenAi chatbase 
stories_Genre = ["Science Fiction", "Fantasy","Mystery/Thriler","Romance","Historical Fiction","Adventure","Dystopian","Young Adult","Horror","Slice of Life"]
stories_made = []
save_output = []

def check_path():
    if not os.path.exists("Output"):
        os.makedirs("test")

# Picks 2 Random Genre
def get_RandomGenre():
    genre =  ", ".join(random.sample(stories_Genre,(len(stories_Genre)//2)-1))
    return "can you create a story involving these genres " + genre + " and remove the Chapter # and just continue it like usual"

# Makes a story genrated from 2 genres
def make_stories():
    stories_made.append({"role": "user", "content": get_RandomGenre()})
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = stories_made
    )
    # save_textoutput.append(response['choices'][0]['message']['content'])
    print("Finished creating the story")
    return response['choices'][0]['message']['content']

def synthesize_text(text): # The Main TTS 
    client = texttospeech.TextToSpeechClient.from_service_account_file("key.json") # Google API KEY to access tts 

    synthesis_input = texttospeech.SynthesisInput(text=text) # Story 

    voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL) 
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    
    rand_num = "".join([str(random.randint(0,5)) for x in range(5)]) # Creates a code so it is different from the others 
    output = f"output{rand_num}.mp3"
    save_output.append(output)
    
    with open(output, "wb") as out: # Makes the MP3 
        out.write(response.audio_content)  
        print(f'Audio content written to file "{output}"')


def create_video():
    name = save_output.pop()
    backg_audio = int(MP3(name).info.length)+1
    clip1 = VideoFileClip("minecraft_gameplay.mp4").subclip(0,backg_audio).fx(vfx.fadein,1).fx(vfx.fadeout, 1).fx(vfx.resize,width=1920,height=1080)
    audio = AudioFileClip(name).fx(afx.audio_fadein, 1)
    combine = clip1
    combine.audio = CompositeAudioClip([audio])
    final_video = f"New_{name.strip('.mp3')}.mp4"
    save_output.append(final_video )
    combine.write_videofile(final_video)
    os.rename(name, f'Output/{name}')
    os.rename(final_video, f'Output/{final_video}')
    


if __name__ == "__main__":  
    check_path()
    synthesize_text(make_stories())
    create_video()

