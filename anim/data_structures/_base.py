from __future__ import annotations
from manim import *
import numpy as np


def hex_to_rgb(hex_color: str) -> ManimColor:
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16) / 255
    g = int(hex_color[2:4], 16) / 255
    b = int(hex_color[4:6], 16) / 255
    return ManimColor([r, g, b])


DIFFICULTY_COLORS: dict[str, str] = {
    "Easy": "#46c6c2",
    "Medium": "#fac31d",
    "Hard": "#f8615c",
}
