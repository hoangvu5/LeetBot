from dotenv import load_dotenv
from settings import (
    CACHE_AUDIO_DIR,
    XI_CHUNK_SIZE,
    XI_MODEL,
    XI_VOICE_ID,
    XI_VOICE_SETTINGS,
)
import logging
import os
import requests

load_dotenv()

log = logging.getLogger(__name__)

_xi_key = os.getenv("XI_API_KEY")
_url = f"https://api.elevenlabs.io/v1/text-to-speech/{XI_VOICE_ID}"


def xi_tts(text: str, audio_path: str) -> None:
    """Convert text to speech via ElevenLabs and write MP3 to audio_path."""
    payload = {
        "model_id": XI_MODEL,
        "text": text,
        "voice_settings": XI_VOICE_SETTINGS,
    }
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": _xi_key,
    }

    response = requests.post(_url, json=payload, headers=headers)
    if not response.ok:
        raise RuntimeError(
            f"ElevenLabs TTS request failed ({response.status_code}): {response.text}"
        )

    os.makedirs(CACHE_AUDIO_DIR, exist_ok=True)
    with open(audio_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=XI_CHUNK_SIZE):
            if chunk:
                f.write(chunk)
    log.info("Audio saved to %s", audio_path)
