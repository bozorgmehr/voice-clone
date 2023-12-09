import streamlit as st
from openai import OpenAI
import os
#from dotenv import load_dotenv

# Load your API key from an environment variable or secret management service
#load_dotenv()  # take environment variables from .env

# Set the API key
os.environ["ELEVEN_API_KEY"] == st.secrets["ELEVEN_API_KEY"]
os.environ["OPENAI_API_KEY"] == st.secrets["OPENAI_API_KEY"]

client = OpenAI()

def speech2text(audio_file):
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text"
    )
    return transcript

def translate(translation, final_text):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are a translater"},
            {"role": "user",
             "content": "Translate the text in" + translation + final_text}
        ]
    )
    return completion.choices[0].message.content
