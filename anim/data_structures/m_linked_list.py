from __future__ import annotations
from manim import *
import numpy as np


class MLinkedList:
    """Visualise a singly-linked list as a horizontal chain of labelled boxes
    connected by arrows, with a trailing "null" label.

    Layout (before scale 0.5):
        [ val ] --> [ val ] --> ... --> null

    Parameters
    ----------
    name:   variable name shown as a label to the left of the list.
    values: Python list of node values (order = head → tail).
    scene:  the active Manim Scene.
    center: where the centre of the whole group is placed.
    """

    _NODE_W: float = 0.7
    _NODE_H: float = 0.5
    _ARROW_LEN: float = 0.4
    _SCALE: float = 0.5

    def __init__(
        self,
        name: str,
        values: list,
        scene: Scene,
        center: np.ndarray = ORIGIN,
        font: str = "CMU Serif",
        stroke_color: ManimColor = WHITE,
        data_color: ManimColor = WHITE,
    ) -> None:
        self.name = name
        self.values = list(values)
        self.scene = scene
        self.center = center
        self.font = font
        self.stroke_color = stroke_color
        self.data_color = data_color

        self._nodes: list[VGroup] = []
        self._arrows: list[VMobject] = []
        self._null_label: Text | None = None

        self.mobject = self._build()

    def _make_node_mob(self, value) -> VGroup:
        box = Rectangle(
            width=self._NODE_W,
            height=self._NODE_H,
            stroke_color=self.stroke_color,
            fill_opacity=0,
            stroke_width=1.5,
        )
        label = Text(str(value), font=self.font, color=self.data_color)
        label.scale_to_fit_width(self._NODE_W * 0.6)
        label.move_to(box.get_center())
        return VGroup(box, label)

    def _build(self) -> VGroup:
        step = self._NODE_W + self._ARROW_LEN
        n = len(self.values)

        name_mob = Text(self.name + " =", font=self.font, color=self.data_color)
        name_mob.scale(0.6)

        self._nodes = []
        self._arrows = []
        parts: list[VMobject] = [name_mob]

        name_right = name_mob.get_right()[0]
        x_offset = name_right + self._NODE_W / 2 + 0.2

        for i, val in enumerate(self.values):
            node_mob = self._make_node_mob(val)
            node_x = x_offset + i * step
            node_mob.move_to(np.array([node_x, 0, 0]))
            self._nodes.append(node_mob)
            parts.append(node_mob)

            if i < n - 1:
                arrow = Arrow(
                    start=np.array([node_x + self._NODE_W / 2, 0, 0]),
                    end=np.array([node_x + self._NODE_W / 2 + self._ARROW_LEN, 0, 0]),
                    buff=0,
                    stroke_width=1.5,
                    color=self.stroke_color,
                    max_tip_length_to_length_ratio=0.3,
                )
                self._arrows.append(arrow)
                parts.append(arrow)

        null_arrow = Arrow(
            start=np.array([x_offset + (n - 1) * step + self._NODE_W / 2, 0, 0]) if n else np.array([x_offset, 0, 0]),
            end=np.array([x_offset + (n - 1) * step + self._NODE_W / 2 + self._ARROW_LEN, 0, 0]) if n else np.array([x_offset + self._ARROW_LEN, 0, 0]),
            buff=0,
            stroke_width=1.5,
            color=self.stroke_color,
            max_tip_length_to_length_ratio=0.3,
        )
        self._null_arrow = null_arrow
        self._null_label = Text("null", font=self.font, color=self.data_color)
        self._null_label.scale(0.5)
        null_label_x = null_arrow.get_end()[0] + self._null_label.width / 2 + 0.1
        self._null_label.move_to(np.array([null_label_x, 0, 0]))
        parts += [null_arrow, self._null_label]

        group = VGroup(*parts)
        group.scale(self._SCALE)
        group.move_to(self.center)
        return group

    def run(self, run_time: float = 1) -> None:
        self.scene.play(Create(self.mobject), run_time=run_time)

    def highlight_node(self, index: int, color: ManimColor = BLUE, run_time: float = 1) -> None:
        if not 0 <= index < len(self._nodes):
            return
        box, label = self._nodes[index][0], self._nodes[index][1]
        self.scene.play(
            box.animate.set_stroke(color=color),
            label.animate.set_color(color=color),
            run_time=run_time,
        )

    def highlight_next(self, index: int, color: ManimColor = BLUE, run_time: float = 1) -> None:
        if not 0 <= index < len(self._arrows):
            return
        self.scene.play(
            self._arrows[index].animate.set_color(color=color),
            run_time=run_time,
        )

    def disappear(self, run_time: float = 1) -> None:
        self.scene.play(FadeOut(self.mobject), run_time=run_time)
