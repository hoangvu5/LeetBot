"""Standalone CLI for Phase 2 only — regenerate and re-render a problem's video.

Useful when you already have a cached problem JSON and only want to redo
the Manim code generation or re-render without re-running Phase 1.
"""
from utils import manim_render
from settings import CACHE_DATA_DIR
import json
import logging
import sys

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)


def main() -> None:
    title_slug = input("Title slug of the problem: ").strip()
    cache_path = f"{CACHE_DATA_DIR}/{title_slug}.json"

    try:
        with open(cache_path, "r", encoding="utf-8") as f:
            cache = json.load(f)
    except FileNotFoundError:
        log.error("Problem cache not found: %s", cache_path)
        sys.exit(1)

    log.info("Generating Manim animation code...")
    construct_body = manim_render.generate_code(cache)
    manim_render.write_scene(construct_body)

    log.info("Rendering video with Manim...")
    rendered_video = manim_render.render(title_slug)
    log.info("Rendered video: %s", rendered_video)


if __name__ == "__main__":
    main()
