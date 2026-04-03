from dotenv import load_dotenv
from settings import CACHE_AUDIO_DIR, GOOGLE_LANGUAGE_CODE, GOOGLE_VOICE_NAME
import base64
import logging
import os
import requests

# Requires GOOGLE_API_KEY env var.
# Enable the Cloud Text-to-Speech API in your Google Cloud project first.
# Voice list: https://cloud.google.com/text-to-speech/docs/voices

load_dotenv()

log = logging.getLogger(__name__)

_TTS_URL = "https://texttospeech.googleapis.com/v1/text:synthesize"
_api_key = os.getenv("GOOGLE_API_KEY")

if not _api_key:
    raise EnvironmentError("GOOGLE_API_KEY is not set. Add it to your .env file.")


def synthesize(text: str, audio_path: str) -> None:
    """Convert text to speech via Google Cloud TTS REST API and write MP3 to audio_path."""
    payload = {
        "input": {"text": text},
        "voice": {
            "languageCode": GOOGLE_LANGUAGE_CODE,
            "name": GOOGLE_VOICE_NAME,
        },
        "audioConfig": {"audioEncoding": "MP3"},
    }

    response = requests.post(_TTS_URL, params={"key": _api_key}, json=payload)
    if not response.ok:
        raise RuntimeError(
            f"Google TTS request failed ({response.status_code}): {response.text}"
        )

    os.makedirs(CACHE_AUDIO_DIR, exist_ok=True)
    with open(audio_path, "wb") as f:
        f.write(base64.b64decode(response.json()["audioContent"]))
    log.info("Audio saved to %s", audio_path)
