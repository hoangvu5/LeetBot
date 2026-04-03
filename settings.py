# settings.py — single source of truth for all LeetBot configuration.
# Edit this file to change models, voices, cache locations, or pipeline behaviour.

# ── Models ────────────────────────────────────────────────────────────────────
GEN_MODEL: str = "gpt-4o"       # OpenAI model used for script and Manim code generation
STT_MODEL: str = "whisper-1"    # OpenAI model used for word-level timestamp extraction

# ── Pipeline toggles ──────────────────────────────────────────────────────────
THUMBNAIL_AUDIO: bool = False   # True → prompt for a custom thumbnail title line
REUSE_AUDIO: bool      = True  # True → skip TTS if audio file already exists in cache
REUSE_PROMPT: bool     = True  # True → skip GPT generation if script already cached
REUSE_TIMESTAMPS: bool = True  # True → skip Whisper if timestamps already exist in cache
REUSE_CODE: bool       = False  # True → skip Manim code generation if code already cached
SOLUTION_IN_CODE: bool = False  # True → include solution code in the generated script

# ── Language ──────────────────────────────────────────────────────────────────
LANGUAGE: str = "Python"        # Programming language for the solution section

# ── TTS provider ─────────────────────────────────────────────────────────────
# "google"      → Google Cloud Text-to-Speech  (requires GOOGLE_API_KEY)
# "elevenlabs"  → ElevenLabs API               (requires XI_API_KEY)
TTS_PROVIDER: str = "google"

# ── Google Cloud TTS ─────────────────────────────────────────────────────────
# Voice reference: https://cloud.google.com/text-to-speech/docs/voices
GOOGLE_LANGUAGE_CODE: str = "en-US"
GOOGLE_VOICE_NAME: str    = "en-US-Journey-D"   # natural, studio-quality male voice

# ── ElevenLabs TTS ───────────────────────────────────────────────────────────
XI_VOICE_ID: str      = "wWWn96OtTHu1sn8SRGEr"   # Hale
XI_MODEL: str         = "eleven_multilingual_v2"
XI_CHUNK_SIZE: int    = 1024
XI_VOICE_SETTINGS: dict = {
    "similarity_boost": 0.75,
    "stability": 0.5,
    "style": 0,
    "use_speaker_boost": True,
}

# ── Video generation model ────────────────────────────────────────────────────
VIDEO_MODEL: str = "gpt-5.4-2026-03-05"   # OpenAI model used specifically for Manim Python code generation

# ── Manim rendering ───────────────────────────────────────────────────────────
# Quality flag passed to the manim CLI:  l=480p15  m=720p30  h=1080p60  k=2160p60
MANIM_QUALITY: str = "h"
MANIM_WIDTH: int   = 1080   # YouTube Shorts: portrait 1080×1920
MANIM_HEIGHT: int  = 1920

# ── Post-processing ───────────────────────────────────────────────────────────
BG_MUSIC_VOLUME: float       = 0.08   # background music level relative to narration (0–1)
CAPTION_WORDS_PER_BLOCK: int = 3      # words grouped into each subtitle card

# ── Cache directories ─────────────────────────────────────────────────────────
CACHE_ROOT: str          = "cache"
CACHE_DATA_DIR: str      = "cache/data"
CACHE_AUDIO_DIR: str     = "cache/audio"
CACHE_PROBLEMS_DIR: str  = "cache/problems"
CACHE_SOLUTION_DIR: str  = "cache/solution"
CACHE_GEN_TEXT_DIR: str  = "cache/generated-text"
CACHE_CODE_DIR: str      = "cache/code"
CACHE_VIDEO_DIR: str     = "cache/video"      # raw manim render output
CACHE_CAPTION_DIR: str   = "cache/captions"   # generated SRT files
CACHE_OUTPUT_DIR: str    = "cache/output"     # final video with music + captions

# ── Scraping ──────────────────────────────────────────────────────────────────
LEETCODE_BASE_URL: str        = "https://leetcode.com/problems/"
PAGE_LOAD_WAIT_S: int         = 7   # seconds to wait for LeetCode page to fully render
DIFFICULTY_CLASSES: list[str] = [
    "text-difficulty-easy",
    "text-difficulty-medium",
    "text-difficulty-hard",
]
