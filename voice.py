import elevenlabs

def generate_voice(text):
    audio = elevenlabs.generate(text=text, voice="Bella")
    elevenlabs.save(audio, "voice_message.mp3")
    return "voice_message.mp3"
