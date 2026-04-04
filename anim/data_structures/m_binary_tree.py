from __future__ import annotations
from manim import *
import numpy as np


class MBinaryTree:
    """Visualise a binary tree from a LeetCode-style level-order list.

    None values represent missing nodes (matching LeetCode's serialisation).

    Example
    -------
    MBinaryTree("root", [3, 9, 20, None, None, 15, 7], scene=self)

         3
        / \\
       9   20
          /  \\
        15    7

    Parameters
    ----------
    name:     variable name shown as a text label.
    array:    level-order list (None = absent node).
    scene:    the active Manim Scene.
    center:   where the top of the tree is placed.
    """

    _NODE_R: float = 0.28
    _LEVEL_H: float = 1.0
    _SCALE: float = 0.9

    def __init__(
        self,
        name: str,
        array: list,
        scene: Scene,
        center: np.ndarray = ORIGIN,
        font: str = "CMU Serif",
        node_color: ManimColor = WHITE,
        edge_color: ManimColor = WHITE,
        data_color: ManimColor = WHITE,
    ) -> None:
        self.name = name
        self.array = array
        self.scene = scene
        self.center = center
        self.font = font
        self.node_color = node_color
        self.edge_color = edge_color
        self.data_color = data_color

        self._node_mobs: dict[int, VGroup] = {}
        self._edge_mobs: dict[tuple[int, int], Line] = {}
        self._positions: dict[int, np.ndarray] = {}

        self.mobject = self._build()

    def _tree_depth(self) -> int:
        n = len(self.array)
        return max(1, n.bit_length())

    def _assign_positions(
        self, idx: int, depth: int, left_x: float, right_x: float, top_y: float
    ) -> None:
        if idx >= len(self.array) or self.array[idx] is None:
            return
        x = (left_x + right_x) / 2
        y = top_y - depth * self._LEVEL_H
        self._positions[idx] = np.array([x, y, 0])
        mid = (left_x + right_x) / 2
        self._assign_positions(2 * idx + 1, depth + 1, left_x, mid, top_y)
        self._assign_positions(2 * idx + 2, depth + 1, mid, right_x, top_y)

    def _build(self) -> VGroup:
        depth = self._tree_depth()
        leaf_spacing = self._NODE_R * 2.5
        tree_half_w = (2 ** (depth - 1)) * leaf_spacing

        self._assign_positions(0, 0, -tree_half_w, tree_half_w, 0.0)

        parts: list[VMobject] = []

        for idx, pos in self._positions.items():
            parent_idx = (idx - 1) // 2
            if idx > 0 and parent_idx in self._positions:
                p_pos = self._positions[parent_idx]
                edge = Line(p_pos, pos, stroke_color=self.edge_color, stroke_width=1.5)
                self._edge_mobs[(parent_idx, idx)] = edge
                parts.append(edge)

        for idx, pos in self._positions.items():
            circle = Circle(
                radius=self._NODE_R,
                stroke_color=self.node_color,
                fill_opacity=0,
                stroke_width=1.5,
            )
            circle.move_to(pos)
            label = Text(str(self.array[idx]), font=self.font, color=self.data_color)
            label.scale_to_fit_width(self._NODE_R * 1.2)
            label.move_to(pos)
            node_mob = VGroup(circle, label)
            self._node_mobs[idx] = node_mob
            parts.append(node_mob)

        name_mob = Text(self.name + " =", font=self.font, color=self.data_color)
        name_mob.scale(0.4)
        parts.append(name_mob)

        group = VGroup(*parts)
        group.scale(self._SCALE)
        group.move_to(self.center)
        name_mob.next_to(group, UL, buff=0.05)

        return group

    def run(self, run_time: float = 1) -> None:
        self.scene.play(Create(self.mobject), run_time=run_time)

    def highlight_node(self, index: int, color: ManimColor = BLUE, run_time: float = 1) -> None:
        if index not in self._node_mobs:
            return
        circle, label = self._node_mobs[index]
        self.scene.play(
            circle.animate.set_stroke(color=color),
            label.animate.set_color(color=color),
            run_time=run_time,
        )

    def highlight_edge(
        self,
        parent_index: int,
        child_index: int,
        color: ManimColor = BLUE,
        run_time: float = 1,
    ) -> None:
        key = (parent_index, child_index)
        if key not in self._edge_mobs:
            return
        self.scene.play(
            self._edge_mobs[key].animate.set_stroke(color=color),
            run_time=run_time,
        )

    def disappear(self, run_time: float = 1) -> None:
        self.scene.play(FadeOut(self.mobject), run_time=run_time)
