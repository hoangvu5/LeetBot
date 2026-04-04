from settings import (
    BG_MUSIC_VOLUME,
    CACHE_CAPTION_DIR,
    CACHE_OUTPUT_DIR,
    CAPTION_WORDS_PER_BLOCK,
    SHOW_SUBTITLES,
)
import logging
import os
import subprocess

log = logging.getLogger(__name__)

# CapCut-style subtitle appearance for 1080x1920 vertical video
_CAPTION_STYLE = (
    "FontName=Arial,"
    "FontSize=70,"
    "Bold=1,"
    "PrimaryColour=&H00FFFFFF,"   # white text
    "OutlineColour=&H00000000,"   # black outline
    "Outline=3,"
    "Shadow=0,"
    "Alignment=2,"                # bottom-centre
    "MarginV=100,"
    "BorderStyle=1"
)


def _to_srt_time(seconds: float) -> str:
    h  = int(seconds // 3600)
    m  = int((seconds % 3600) // 60)
    s  = int(seconds % 60)
    ms = int(round((seconds % 1) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def generate_srt(timestamps: list[dict], title_slug: str) -> str:
    """Group word timestamps into subtitle blocks and write an SRT file.

    Returns the path to the written SRT file.
    """
    os.makedirs(CACHE_CAPTION_DIR, exist_ok=True)
    srt_path = f"{CACHE_CAPTION_DIR}/{title_slug}.srt"

    blocks = [
        timestamps[i : i + CAPTION_WORDS_PER_BLOCK]
        for i in range(0, len(timestamps), CAPTION_WORDS_PER_BLOCK)
    ]

    entries: list[str] = []
    for idx, block in enumerate(blocks, 1):
        start = _to_srt_time(block[0]["start"])
        end   = _to_srt_time(block[-1]["end"])
        text  = " ".join(w["word"] for w in block)
        entries.append(f"{idx}\n{start} --> {end}\n{text}")

    with open(srt_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(entries) + "\n")

    log.info("SRT written to %s", srt_path)
    return srt_path


def finalize(
    video_path: str,
    narration_path: str,
    music_path: str,
    srt_path: str,
    title_slug: str,
) -> str:
    """Combine silent manim video with narration + background music, then optionally burn captions.

    Pipeline:
        Pass 1 — filter_complex: mix narration + bg music, fix SAR → output MP4
        Pass 2 (SHOW_SUBTITLES only) — burn SRT captions onto pass-1 output

    Returns the path to the final output video.
    """
    os.makedirs(CACHE_OUTPUT_DIR, exist_ok=True)
    output_path = f"{CACHE_OUTPUT_DIR}/{title_slug}.mp4"

    has_music = bool(music_path and os.path.exists(music_path))
    if not has_music and music_path:
        log.warning("Background music not found at '%s' — skipping.", music_path)

    # ── Pass 1: mix audio + fix SAR ──────────────────────────────────────────
    cmd = ["ffmpeg", "-y", "-i", video_path, "-i", narration_path]
    if has_music:
        cmd += ["-i", music_path]
        audio_fc = (
            f"[1:a]aresample=44100[nar];"
            f"[2:a]volume={BG_MUSIC_VOLUME},aresample=44100[bg];"
            "[nar][bg]amix=inputs=2:duration=first:dropout_transition=2[aout]"
        )
    else:
        audio_fc = "[1:a]aresample=44100[aout]"

    filter_complex = f"{audio_fc};[0:v]setsar=1[vout]"

    cmd += [
        "-filter_complex", filter_complex,
        "-map", "[vout]",
        "-map", "[aout]",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-b:a", "192k",
        output_path,
    ]

    log.info("Mixing audio and encoding video...")
    _run(cmd)

    # ── Pass 2: burn captions (optional) ────────────────────────────────────
    if SHOW_SUBTITLES:
        sub_path = f"{CACHE_OUTPUT_DIR}/{title_slug}_sub.mp4"
        srt_abs  = os.path.abspath(srt_path).replace("\\", "/").replace(":", "\\:")
        log.info("Burning captions...")
        _run([
            "ffmpeg", "-y",
            "-i", output_path,
            "-vf", f"subtitles='{srt_abs}':force_style='{_CAPTION_STYLE}'",
            "-map", "0:v",
            "-map", "0:a",
            "-c:v", "libx264",
            "-c:a", "copy",
            sub_path,
        ])
        os.replace(sub_path, output_path)

    log.info("Final video saved to %s", output_path)
    return output_path


def _run(cmd: list[str]) -> None:
    result = subprocess.run(cmd)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed (exit {result.returncode}): {' '.join(cmd)}")
