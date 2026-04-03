from utils import chatgpt, selenium, manim_render, post_process
from utils import google_tts, xi_labs
from settings import (
    CACHE_AUDIO_DIR,
    CACHE_DATA_DIR,
    CACHE_GEN_TEXT_DIR,
    CACHE_SOLUTION_DIR,
    GEN_MODEL,
    LANGUAGE,
    REUSE_AUDIO,
    REUSE_PROMPT,
    REUSE_TIMESTAMPS,
    STT_MODEL,
    THUMBNAIL_AUDIO,
    TTS_PROVIDER,
)
import json
import logging
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)


def _tts(text: str, audio_path: str) -> None:
    """Dispatch to the configured TTS provider."""
    if TTS_PROVIDER == "google":
        google_tts.synthesize(text, audio_path)
    elif TTS_PROVIDER == "elevenlabs":
        xi_labs.xi_tts(text, audio_path)
    else:
        raise ValueError(f"Unknown TTS_PROVIDER '{TTS_PROVIDER}' in settings.py")


def main() -> None:
    # ── Phase 1: Content generation ──────────────────────────────────────────
    output: dict = {}

    title, title_slug, description, example, example_dict, num, difficulty = selenium.scrape()
    output["title"]       = title
    output["title_slug"]  = title_slug
    output["number"]      = num
    output["difficulty"]  = difficulty
    output["description"] = description
    output["example"]     = example_dict

    sections: dict[str, str] = {}

    if THUMBNAIL_AUDIO:
        audio_thumbnail = input("Enter thumbnail title: ")
        sections["title"] = audio_thumbnail + ". "
    else:
        sections["title"] = f"LeetCode Problem {num}: {title}. "

    solution = ""
    solution_path = f"{CACHE_SOLUTION_DIR}/{title_slug}.txt"
    if os.path.exists(solution_path):
        with open(solution_path, "r", encoding="utf-8") as f:
            solution = f.read()

    log.info("Generating script with %s...", GEN_MODEL)
    gen_path = f"{CACHE_GEN_TEXT_DIR}/{title_slug}.txt"
    if os.path.exists(gen_path) and REUSE_PROMPT:
        with open(gen_path, "r", encoding="utf-8") as f:
            response = f.read()
    else:
        prompt = chatgpt.generate_prompt(description, example, solution, language=LANGUAGE)
        response = chatgpt.complete_chat(prompt, GEN_MODEL, title_slug)

    postprocessed = chatgpt.postprocessing(response)
    for key, value in postprocessed.items():
        sections[key] = value

    output["audio"] = {}
    script = ""
    for key, value in sections.items():
        if key != "solution":
            script += value
    output["script"] = script

    log.info("Generating narration audio via %s...", TTS_PROVIDER)
    audio_path = f"{CACHE_AUDIO_DIR}/{title_slug}.mp3"
    if not (os.path.exists(audio_path) and REUSE_AUDIO):
        _tts(script, audio_path)
    output["audio"]["script"] = audio_path

    solution_audio_path = f"{CACHE_AUDIO_DIR}/solution_{LANGUAGE}.mp3"
    if not os.path.exists(solution_audio_path):
        _tts(f"Here's the solution written in {LANGUAGE}.", solution_audio_path)
    output["audio"]["solution"] = solution_audio_path

    output["audio"]["background"] = f"{CACHE_AUDIO_DIR}/happy-bg-1.mp3"

    os.makedirs(CACHE_DATA_DIR, exist_ok=True)
    cache_path = f"{CACHE_DATA_DIR}/{title_slug}.json"

    # Load existing timestamps from cache JSON if available and reuse is enabled
    _existing_timestamps: list | None = None
    if REUSE_TIMESTAMPS and os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                _cached = json.load(f)
            _existing_timestamps = _cached.get("timestamps")
        except (json.JSONDecodeError, KeyError):
            pass

    if _existing_timestamps:
        log.info("Reusing cached audio timestamps.")
        output["timestamps"] = _existing_timestamps
    else:
        log.info("Extracting audio timestamps...")
        output["timestamps"] = chatgpt.get_timestamps(audio_path, STT_MODEL, script=script)

    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)
    log.info("Phase 1 complete — cache saved to %s", cache_path)

    # ── Phase 2: Manim code generation and rendering ──────────────────────────
    log.info("Generating Manim animation code...")
    construct_body = manim_render.generate_code(output)
    manim_render.write_scene(construct_body)

    log.info("Rendering video with Manim...")
    rendered_video = manim_render.render(title_slug)

    # ── Phase 3: Post-processing (audio mix + captions) ───────────────────────
    log.info("Generating captions...")
    srt_path = post_process.generate_srt(output["timestamps"], title_slug)

    log.info("Finalizing video...")
    final_video = post_process.finalize(
        video_path     = rendered_video,
        narration_path = output["audio"]["script"],
        music_path     = output["audio"]["background"],
        srt_path       = srt_path,
        title_slug     = title_slug,
    )

    log.info("Done. Final video: %s", final_video)


if __name__ == "__main__":
    main()
