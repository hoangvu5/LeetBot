from __future__ import annotations
from manim import *
import numpy as np


class MText:
    def __init__(
        self,
        text: str,
        scene: Scene,
        center: np.ndarray = ORIGIN,
        font: str = "CMU Serif",
        data_color: ManimColor = WHITE,
    ) -> None:
        self.text = text
        self.scene = scene
        self.center = center
        self.font = font
        self.data_color = data_color

        self.mobject = Text(str(self.text), font=self.font, color=self.data_color)
        self.mobject.scale(0.45)
        self.mobject.move_to(self.center)

    def run(self, run_time: float = 1) -> None:
        self.scene.play(Create(self.mobject), run_time=run_time)

    def edit(self, new_text: str, run_time: float = 1) -> None:
        old = self.mobject
        self.text = new_text
        self.mobject = Text(str(self.text), font=self.font, color=self.data_color)
        self.mobject.scale(0.5)
        self.mobject.move_to(old.get_center())
        self.scene.play(ReplacementTransform(old, self.mobject), run_time=run_time)

    def disappear(self, run_time: float = 1) -> None:
        self.scene.play(FadeOut(self.mobject), run_time=run_time)
