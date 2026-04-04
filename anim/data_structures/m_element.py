from __future__ import annotations
from manim import *
import numpy as np


class MElement:
    def __init__(
        self,
        data: int | float | str,
        index: int,
        center: np.ndarray = ORIGIN,
        width: float = 0.4,
        font: str = "CMU Serif",
        stroke_color: ManimColor = WHITE,
        data_color: ManimColor = WHITE,
        show_index: bool = True,
    ) -> None:
        self.data = data
        self.index = index
        self.center = center
        self.width = width
        self.font = font
        self.stroke_color = stroke_color
        self.data_color = data_color
        self.show_index = show_index

        self.mdata = Text(str(data), color=self.data_color, font=self.font)
        self.mdata.move_to(self.center)

        self.mrectangle = RoundedRectangle(
            height=self.width,
            width=self.width,
            stroke_color=self.stroke_color,
            fill_opacity=0,
            stroke_width=1,
            corner_radius=0.2,
        )
        self.mrectangle.move_to(self.center)

        self.mindex = Text(str(self.index), color=self.data_color, font=self.font)
        self.mindex.scale(0.5)
        self.mindex.next_to(self.mrectangle, UP, buff=0.2)

        self.mobject = VGroup(self.mdata, self.mrectangle, self.mindex)
