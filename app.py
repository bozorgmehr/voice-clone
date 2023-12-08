import streamlit as st
from voiceclone import *
from elevenlabs import set_api_key, voices
from audiorecorder import audiorecorder
import re
import numpy as np
from dotenv import load_dotenv
import os

# Load your API key from an environment variable or secret management service
#load_dotenv()  # take environment variables from .env

# Set the API key
#elevanlabkey = os.environ["elevenlabs-api-key"]

#set_api_key()

# Everything is accessible via the st.secrets dict:
st.write("elevenlabs-api-key:", st.secrets["elevenlabs-api-key"])

# And the root-level secrets are also accessible as environment variables:
st.write(
    "Has environment variables been set:",
    os.environ["elevenlabs-api-key"] == st.secrets["elevenlabs-api-key"],
)

def get_voices():
    all_voices = voices()
    voice_name = []
    for i in range(len(all_voices)):
        data_str = str(all_voices[i])

        # Use regular expression to extract the value associated with 'name'
        match = re.search(r"name='([^']+)'", data_str)
        if match:
            name = match.group(1)
            voice_name.append(name)

        else:
            print("Name not found in the string.")

    voice_name = np.array(voice_name)
    print(voice_name)
    return voice_name


if __name__ == "__main__":

    st.header("Voice Clone")

    action = st.radio(
        "What do you want to do?",
        ["Create a text with a available voice", "Create a custom voice"],
        captions=["Put the text you want", "Let's do it."])

    if action == 'Create a text with a available voice':

        with st.form("Info", clear_on_submit=True):
            text = st.text_area('Type here the text you want.', max_chars=5000)
            voice_selection = st.selectbox("Select a voice", get_voices())
            submitted = st.form_submit_button("Submit")
            if submitted:
                st.audio(stream_audio(text, voice_name=voice_selection))
    else:
        new_voice_name = st.text_area('Name')

        description = st.text_area("Ler este texto. Se quiser editar, coloque outro texto.",
        "It was the best of times, it was the worst of times, it was the age of "
        "wisdom, it was the age of foolishness, it was the epoch of belief, it "
        "was the epoch of incredulity, it was the season of Light, it was the "
        "season of Darkness, it was the spring of hope, it was the winter of "
        "despair, (...)")  # Optional

        if description:

            audio = audiorecorder("Click to record", "Click to stop recording")

            if len(audio) > 0:
                # To play audio in frontend:
                st.audio(audio.export().read())

                # To save audio to a file, use pydub export method:
                audio.export("audio.wav", format="wav")

                # To get audio properties, use pydub AudioSegment properties:
                st.write(
                    f"Frame rate: {audio.frame_rate}, Frame width: {audio.frame_width}, Duration: {audio.duration_seconds} seconds")

                files = ['./audio.wav']

                new_voice = voice_clone(new_voice_name, 'A custom voice', files)

                if new_voice:
                    text_new = st.text_input('Type here the text you want.')

                    if text_new:
                        st.audio(stream_audio(text_new, voice_name=new_voice_name))



