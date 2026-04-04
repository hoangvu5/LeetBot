from __future__ import annotations
from manim import *
import numpy as np


class MVariable:
    def __init__(
        self,
        name: str,
        variable: int | float | str,
        scene: Scene,
        center: np.ndarray = ORIGIN,
        font: str = "CMU Serif",
        data_color: ManimColor = WHITE,
    ) -> None:
        self.name = name
        self.variable = variable
        self.center = center
        self.font = font
        self.data_color = data_color
        self.scene = scene

        self.mobject = Text(f"{name} = {variable}", font=self.font)
        self.mobject.scale(0.5)
        self.mobject.move_to(self.center)

    def run(self, run_time: float = 1) -> None:
        self.scene.play(Create(self.mobject), run_time=run_time)

    def highlight_variable(self, color: ManimColor = BLUE, run_time: float = 1) -> None:
        self.scene.play(self.mobject.animate.set_color(color=color), run_time=run_time)

    def disappear(self, run_time: float = 1) -> None:
        self.scene.play(FadeOut(self.mobject), run_time=run_time)
