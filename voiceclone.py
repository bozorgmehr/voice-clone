from elevenlabs import set_api_key, generate, clone,  stream

#set_api_key("7cbe591f5982171ee2adb23d29204db2")

def voice_default(text, voice_name, model):
    audio = generate(
        text=text,
        voice=voice_name,
        model=model
    )
    return audio


def voice_clone(name, description, files):
    voice = clone(
        name=name,
        description=description,  # Optional
        files=files,
    )
    return voice


def voice_custom(text, voice_name):
    audio = generate(
        text=text,
        voice=voice_name,
        model = "eleven_multilingual_v2")
    return audio

def stream_audio(text_stream, voice_name):
    audio_stream = generate(
        text=text_stream,
        voice=voice_name,
        model="eleven_multilingual_v2",
        stream=True)

    return stream(audio_stream)


##main
##using default voice
#text_stream = "Olá! O meu nome é Joana Sousa."
#voice_input = "Bella"
#model = "eleven_multilingual_v2"
#output = voice_default(text_input, voice_input, model)
#output = voice_custom(text_input, voice_id)
#play(output)

#audio_stream = stream_audio(text_stream, voice_id)

# TO TRAIN
# name = "Alex",
# description = "An old American male voice with a slight hoarseness in his throat. Perfect for news",  # Optional
# files = ["./sample_0.mp3", "./sample_1.mp3", "./sample_2.mp3"]
# voice = voice_clone(name, description, files)
# audio = generate(text="Hi! I'm a cloned voice!", voice=voice)
