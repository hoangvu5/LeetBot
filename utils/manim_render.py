from pathlib import Path
from settings import CACHE_CODE_DIR, CACHE_VIDEO_DIR, MANIM_CACHE, MANIM_HEIGHT, MANIM_QUALITY, MANIM_WIDTH, REUSE_CODE, VIDEO_MODEL
from utils import chatgpt
import logging
import os
import subprocess
import sys
import textwrap

log = logging.getLogger(__name__)

_ANIM_DIR   = Path("anim")
_SCENE_FILE = _ANIM_DIR / "rendering.py"
_SCENE_NAME = "MProblem"

_SCENE_TEMPLATE = """\
from manim import *
import numpy as np
from data_structures import *

class MProblem(Scene):
    def construct(self):
{body}
"""


def _extract_python_block(text: str) -> str:
    # Try ```python fence first, then plain ``` fence, then treat whole response as code
    for fence in ("```python", "```"):
        start = text.find(fence)
        if start != -1:
            start += len(fence)
            end = text.find("```", start)
            if end != -1:
                return text[start:end].strip()
    # No fences found — assume entire response is raw code
    log.warning("No code fence found in model response; using raw output as code.")
    return text.strip()


def _strip_construct_header(code: str) -> str:
    """Remove 'def construct(self):' wrapper if the model included it in its output."""
    lines = code.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith("def construct"):
            body_lines = lines[i + 1:]
            # Strip exactly one level of indentation (4 spaces or 1 tab)
            dedented = []
            for ln in body_lines:
                if ln.startswith("    "):
                    dedented.append(ln[4:])
                elif ln.startswith("\t"):
                    dedented.append(ln[1:])
                else:
                    dedented.append(ln)
            return "\n".join(dedented)
    return code


def generate_code(cache: dict) -> str:
    """Return the construct() body, using cache if REUSE_CODE is set and cache exists."""
    title_slug = cache["title_slug"]
    os.makedirs(CACHE_CODE_DIR, exist_ok=True)
    code_path = f"{CACHE_CODE_DIR}/{title_slug}.txt"

    if REUSE_CODE and os.path.exists(code_path):
        log.info("Reusing cached Manim code from %s", code_path)
        with open(code_path, "r", encoding="utf-8") as f:
            return f.read()

    prompt = chatgpt.generate_video_prompt(cache)
    response = chatgpt.complete_video_chat(prompt, VIDEO_MODEL)
    code = _strip_construct_header(_extract_python_block(response))

    with open(code_path, "w", encoding="utf-8") as f:
        f.write(code)
    log.info("Manim code cached to %s", code_path)
    return code


def write_scene(construct_body: str) -> None:
    """Wrap the construct() body in a full MProblem scene and write anim/rendering.py."""
    indented = textwrap.indent(construct_body, "        ")
    _SCENE_FILE.write_text(_SCENE_TEMPLATE.format(body=indented), encoding="utf-8")
    log.info("Scene written to %s", _SCENE_FILE)


def render(title_slug: str) -> str:
    """Run the manim CLI and return the absolute path to the rendered MP4."""
    media_dir = Path(CACHE_VIDEO_DIR).resolve()
    cmd = [
        sys.executable, "-m", "manim",
        f"-q{MANIM_QUALITY}",
        "--media_dir", str(media_dir),
    ]
    if not MANIM_CACHE:
        cmd.append("--disable_caching")
    cmd += ["rendering.py", _SCENE_NAME]
    log.info("Running: %s", " ".join(cmd))
    result = subprocess.run(cmd, cwd=str(_ANIM_DIR.resolve()))
    if result.returncode != 0:
        raise RuntimeError("Manim rendering failed — see output above.")

    matches = list(Path(CACHE_VIDEO_DIR).rglob(f"{_SCENE_NAME}.mp4"))
    if not matches:
        raise FileNotFoundError(
            f"Rendered {_SCENE_NAME}.mp4 not found under {CACHE_VIDEO_DIR}"
        )
    mp4_path = max(matches, key=lambda p: p.stat().st_mtime)
    log.info("Rendered video: %s", mp4_path)
    return str(mp4_path)
