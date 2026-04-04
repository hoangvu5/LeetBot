from __future__ import annotations
from manim import *
import numpy as np

from ._base import DIFFICULTY_COLORS, hex_to_rgb


class MTitle:
    def __init__(
        self,
        title: str,
        subtitle: str,
        scene: Scene,
        center: np.ndarray = ORIGIN,
        color: ManimColor = WHITE,
        font: str = "CMU Serif",
    ) -> None:
        self.title = title
        self.subtitle = subtitle
        self.center = center
        self.color = color
        self.font = font
        self.scene = scene

        self.mtitle = Text(str(title), color=self.color, font=self.font)
        self.mtitle.move_to(self.center)

        subtitle_hex = DIFFICULTY_COLORS.get(self.subtitle, "#ffffff")
        self.msubtitle = Text(
            f"Difficulty: {self.subtitle}",
            font=self.font,
            t2c={self.subtitle: hex_to_rgb(subtitle_hex)},
        )
        self.msubtitle.scale(0.5)
        self.msubtitle.move_to(self.center + DOWN * 0.75)

    def run(self, run_time: float = 1) -> None:
        self.scene.play(Create(self.mtitle), Create(self.msubtitle), run_time=0.25)
        self.scene.wait(run_time - 0.5)
        self.scene.play(
            self.mtitle.animate.move_to(UP * 3.25).scale(0.25),
            self.msubtitle.animate.move_to(UP * 2.90).scale(0.5),
            run_time=0.25,
        )
