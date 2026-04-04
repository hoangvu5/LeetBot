from __future__ import annotations
from manim import *
import numpy as np

from .m_element import MElement


class MStack:
    def __init__(
        self,
        name: str,
        stack: list,
        scene: Scene,
        center: np.ndarray = ORIGIN,
        width: float = 1,
        font: str = "CMU Serif",
        margin: float = 0.1,
        stroke_color: ManimColor = WHITE,
        data_color: ManimColor = WHITE,
    ) -> None:
        self.name = name + " = "
        self.stack = stack
        self.center = center
        self.width = width
        self.font = font
        self.margin = margin
        self.stroke_color = stroke_color
        self.data_color = data_color
        self.scene = scene

        self.mtitle = Text(str(self.name), color=self.data_color, font=self.font)
        title_x = self.center[0] - config["frame_width"] / 2 + 3 * self.margin + self.mtitle.width / 2
        self.mtitle.move_to(np.array([title_x, self.center[1], 0]))

        stack_start_x = self.center[0] - config["frame_width"] / 2 + 6 * self.margin + self.mtitle.width
        self.top_center = np.array([stack_start_x, self.center[1], 0])

        # Bounding box: two horizontal rails + left vertical wall
        left_x = self.center[0] - config["frame_width"] / 2 + 5 * self.margin + self.mtitle.width
        right_x = self.center[0] + config["frame_width"] / 2 - 3 * self.margin
        top_y = self.center[1] + self.width + self.margin
        bottom_y = self.center[1] - self.width - self.margin

        top_rail    = Line(np.array([left_x, top_y, 0]),    np.array([right_x, top_y, 0]),    stroke_color=stroke_color)
        bottom_rail = Line(np.array([left_x, bottom_y, 0]), np.array([right_x, bottom_y, 0]), stroke_color=stroke_color)
        left_wall   = Line(np.array([left_x, top_y, 0]),    np.array([left_x, bottom_y, 0]),  stroke_color=stroke_color)
        self.mbox = VGroup(top_rail, bottom_rail, left_wall)

        self.mstack: list[MElement] = []
        for value in self.stack:
            melement = MElement(
                data=value,
                index=len(self.mstack),
                center=self.top_center.copy(),
                width=self.width,
                font=self.font,
                stroke_color=self.stroke_color,
                data_color=self.data_color,
                show_index=False,
            )
            self.mstack.append(melement)
            self.top_center[0] += self.width + self.margin

        self.mobject = VGroup(self.mtitle, self.mbox, *[e.mobject for e in self.mstack])
        self.mobject.scale(0.5)

    def run(self, run_time: float = 1) -> None:
        self.scene.play(Create(self.mobject), run_time=run_time)

    def highlight_top(self, color: ManimColor = BLUE, run_time: float = 1) -> None:
        if not self.mstack:
            return
        top = self.mstack[-1]
        self.scene.play(
            top.mrectangle.animate.set_stroke(color=color),
            top.mdata.animate.set_color(color=color),
            run_time=run_time,
        )

    def push(self, value, run_time: float = 1) -> None:
        melement = MElement(
            data=value,
            index=len(self.mstack),
            center=self.top_center.copy(),
            width=self.width,
            font=self.font,
            stroke_color=self.stroke_color,
            data_color=self.data_color,
            show_index=False,
        )
        self.mstack.append(melement)
        self.top_center[0] += self.width + self.margin
        self.mobject.add(melement.mobject)
        self.scene.play(FadeIn(melement.mobject), run_time=run_time)

    def pop(self, run_time: float = 1) -> int | float | str:
        if not self.mstack:
            return -1
        top = self.mstack.pop()
        self.top_center[0] -= self.width + self.margin
        self.scene.play(FadeOut(top.mobject), run_time=run_time)
        return top.data

    def top(self) -> int | float | str:
        if not self.mstack:
            return -1
        return self.mstack[-1].data

    def disappear(self, run_time: float = 1) -> None:
        self.scene.play(FadeOut(self.mobject), run_time=run_time)
