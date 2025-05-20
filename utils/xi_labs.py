import requests
import os

CHUNK_SIZE = 1024
xi_key = os.getenv("XI_API_KEY")

# voice_id = "FdwfwWtVwj4Q6sR0vunC" # Myriam
# voice_id = "Xb7hH8MSUJpSbSDYk0k2" # Alice
# voice_id = "UEKYgullGqaF0keqT8Bu" # Chris
voice_id = "BtWabtumIemAotTjP5sk" # Robert
# voice_id = "TV98XJgJjJZWhXiSKmhJ" # My Voice
url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

def xi_tts(text, audio_path):
    payload = {
        "model_id": "eleven_multilingual_v2",
        "text": text,
        "voice_settings": {
            "similarity_boost": 0.75,
            "stability": 0.5,
            "style": 0,
            "use_speaker_boost": True
        }
    }

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": xi_key
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Request was successful, status code:", response.status_code)
    else:
        print("Request failed, status code:", response.status_code)
        print("Response content:", response.text)
        return

    directory = 'cache/audio'
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    with open(audio_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)
