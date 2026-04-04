from __future__ import annotations
from manim import *
import numpy as np

from .m_element import MElement


class MArray:
    def __init__(
        self,
        name: str,
        array: list,
        scene: Scene,
        center: np.ndarray = ORIGIN,
        width: float = 1,
        font: str = "CMU Serif",
        margin: float = 0.1,
        stroke_color: ManimColor = WHITE,
        data_color: ManimColor = WHITE,
        show_index: bool = True,
    ) -> None:
        self.name = name + " = "
        self.array = array
        self.center = center
        self.width = width
        self.font = font
        self.margin = margin
        self.stroke_color = stroke_color
        self.data_color = data_color
        self.show_index = show_index
        self.scene = scene

        self.mtitle = Text(str(self.name), color=self.data_color, font=self.font)

        count = len(array)
        total_width = (count * self.width) + ((count + 2) * self.margin) + self.mtitle.width
        self.mtitle.move_to(
            np.array([self.center[0] - total_width / 2 + self.mtitle.width / 2, self.center[1], 0])
        )

        self.marray: list[MElement] = []
        start_x = self.center[0] - total_width / 2 + self.mtitle.width + self.width / 2 + self.margin * 3
        for idx, value in enumerate(self.array):
            x = start_x + idx * (self.width + self.margin)
            melement = MElement(
                data=value,
                index=idx,
                center=np.array([x, self.center[1], 0]),
                width=self.width,
                font=self.font,
                stroke_color=self.stroke_color,
                data_color=self.data_color,
                show_index=self.show_index,
            )
            self.marray.append(melement)

        self.mobject = VGroup(self.mtitle, *[e.mobject for e in self.marray])
        self.mobject.scale(0.5)

    def run(self, run_time: float = 1) -> None:
        self.scene.play(Create(self.mobject), run_time=run_time)

    def highlight_element(self, index: int, color: ManimColor = BLUE, run_time: float = 1) -> None:
        self.scene.play(
            self.marray[index].mrectangle.animate.set_stroke(color=color),
            self.marray[index].mdata.animate.set_color(color=color),
            run_time=run_time,
        )

    def highlight_range(self, start: int, end: int, color: ManimColor = BLUE, run_time: float = 1) -> None:
        animations = [
            self.marray[i].mrectangle.animate.set_stroke(color=color) for i in range(start, end + 1)
        ] + [
            self.marray[i].mdata.animate.set_color(color=color) for i in range(start, end + 1)
        ]
        self.scene.play(*animations, run_time=run_time)

    def highlight_elements(self, indices: list[int], color: ManimColor = BLUE, run_time: float = 1) -> None:
        animations = [
            self.marray[i].mrectangle.animate.set_stroke(color=color) for i in indices
        ] + [
            self.marray[i].mdata.animate.set_color(color=color) for i in indices
        ]
        self.scene.play(*animations, run_time=run_time)

    def disappear(self, run_time: float = 1) -> None:
        self.scene.play(FadeOut(self.mobject), run_time=run_time)
