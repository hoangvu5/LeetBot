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


class MMap:
    def __init__(
        self,
        name: str,
        map: dict,
        scene: Scene,
        center: np.ndarray = ORIGIN,
        font: str = "CMU Serif",
        data_color: ManimColor = WHITE,
    ) -> None:
        self.name = name
        self.map = map
        self.scene = scene
        self.center = center
        self.font = font
        self.data_color = data_color

        self.mobject = self._build_mobject()

    def _build_mobject(self) -> Text:
        map_str = self.name + " = {" + ", ".join(f"{k}: {v}" for k, v in self.map.items()) + "}"
        mob = Text(map_str, font=self.font)
        mob.scale(0.5)
        mob.move_to(self.center)
        return mob

    def run(self, run_time: float = 1) -> None:
        self.scene.play(Create(self.mobject), run_time=run_time)

    def _replace_mobject(self, new_mob: Text, run_time: float) -> None:
        old = self.mobject
        self.mobject = new_mob
        self.scene.play(ReplacementTransform(old, self.mobject), run_time=run_time)

    def insert_element(self, key, value, run_time: float = 1) -> None:
        self.map[key] = value
        map_str = self.name + " = {" + ", ".join(f"{k}: {v}" for k, v in self.map.items()) + "}"
        new_mob = Text(map_str, font=self.font)
        new_mob.scale(0.5)
        new_mob.move_to(self.mobject.get_center())
        self._replace_mobject(new_mob, run_time)

    def remove_element(self, key, run_time: float = 1) -> None:
        del self.map[key]
        map_str = "{" + ", ".join(f"{k}: {v}" for k, v in self.map.items()) + "}"
        new_mob = Text(map_str, font=self.font)
        new_mob.scale(0.5)
        new_mob.move_to(self.mobject.get_center())
        self._replace_mobject(new_mob, run_time)

    def highlight_element(self, key, color: ManimColor = BLUE, run_time: float = 1) -> None:
        if key not in self.map:
            return
        map_str = self.name + " = {" + ", ".join(f"{k}: {v}" for k, v in self.map.items()) + "}"
        new_mob = Text(map_str, font=self.font, t2c={str(key): color, str(self.map[key]): color})
        new_mob.scale(0.5)
        new_mob.move_to(self.mobject.get_center())
        self._replace_mobject(new_mob, run_time)

    def highlight(self, color: ManimColor = BLUE, run_time: float = 1) -> None:
        self.scene.play(self.mobject.animate.set_color(color=color), run_time=run_time)

    def disappear(self, run_time: float = 1) -> None:
        self.scene.play(FadeOut(self.mobject), run_time=run_time)


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
        stack_total_width = config["frame_width"] - 8 * self.margin - self.mtitle.width

        # Bounding box: two horizontal rails + left vertical wall
        left_x = self.center[0] - config["frame_width"] / 2 + 5 * self.margin + self.mtitle.width
        right_x = self.center[0] + config["frame_width"] / 2 - 3 * self.margin
        top_y = self.center[1] + self.width + self.margin
        bottom_y = self.center[1] - self.width - self.margin

        top_rail = Line(np.array([left_x, top_y, 0]), np.array([right_x, top_y, 0]), stroke_color=stroke_color)
        bottom_rail = Line(np.array([left_x, bottom_y, 0]), np.array([right_x, bottom_y, 0]), stroke_color=stroke_color)
        left_wall = Line(np.array([left_x, top_y, 0]), np.array([left_x, bottom_y, 0]), stroke_color=stroke_color)
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


# ---------------------------------------------------------------------------
# MLinkedList
# ---------------------------------------------------------------------------

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

    _NODE_W: float = 0.7   # box width
    _NODE_H: float = 0.5   # box height
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

        # Internal per-node mobject tracking (box + label VGroup, arrow)
        self._nodes: list[VGroup] = []    # each node's box+text VGroup
        self._arrows: list[VMobject] = [] # arrows between nodes
        self._null_label: Text | None = None

        self.mobject = self._build()

    # ------------------------------------------------------------------
    # Build helpers
    # ------------------------------------------------------------------

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
        """Construct the full mobject from self.values."""
        step = self._NODE_W + self._ARROW_LEN
        n = len(self.values)
        total_w = n * self._NODE_W + max(n - 1, 0) * self._ARROW_LEN

        # Name label
        name_mob = Text(self.name + " =", font=self.font, color=self.data_color)
        name_mob.scale(0.6)

        # Build nodes left → right starting from x=0 in local coords
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

        # "null" terminator
        null_x = x_offset + n * step - self._ARROW_LEN / 2 if n > 0 else x_offset
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
        null_label_x = (null_arrow.get_end()[0] + self._null_label.width / 2 + 0.1)
        self._null_label.move_to(np.array([null_label_x, 0, 0]))
        parts += [null_arrow, self._null_label]

        group = VGroup(*parts)
        group.scale(self._SCALE)
        group.move_to(self.center)
        return group

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self, run_time: float = 1) -> None:
        self.scene.play(Create(self.mobject), run_time=run_time)

    def highlight_node(self, index: int, color: ManimColor = BLUE, run_time: float = 1) -> None:
        """Highlight the box and value of the node at position `index`."""
        if not 0 <= index < len(self._nodes):
            return
        node_mob = self._nodes[index]
        box, label = node_mob[0], node_mob[1]
        self.scene.play(
            box.animate.set_stroke(color=color),
            label.animate.set_color(color=color),
            run_time=run_time,
        )

    def highlight_next(self, index: int, color: ManimColor = BLUE, run_time: float = 1) -> None:
        """Highlight the arrow leading out of node at position `index`."""
        if not 0 <= index < len(self._arrows):
            return
        self.scene.play(
            self._arrows[index].animate.set_color(color=color),
            run_time=run_time,
        )

    def disappear(self, run_time: float = 1) -> None:
        self.scene.play(FadeOut(self.mobject), run_time=run_time)


# ---------------------------------------------------------------------------
# MBinaryTree
# ---------------------------------------------------------------------------

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

    _NODE_R: float = 0.28     # node circle radius
    _LEVEL_H: float = 1.0     # vertical distance between levels
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

        # Populated by _build(): index → (circle, label) VGroup
        self._node_mobs: dict[int, VGroup] = {}
        # (parent_idx, child_idx) → Line
        self._edge_mobs: dict[tuple[int, int], Line] = {}
        # index → np.ndarray position (in unscaled local coords)
        self._positions: dict[int, np.ndarray] = {}

        self.mobject = self._build()

    # ------------------------------------------------------------------
    # Build helpers
    # ------------------------------------------------------------------

    def _tree_depth(self) -> int:
        """Maximum depth of the array-represented tree."""
        depth = 0
        i = 0
        while i < len(self.array):
            depth += 1
            i = 2 * i + 1  # jump to next level's first index (approx)
        # Compute via bit length of len
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
        # Tree width = 2^(depth-1) leaf slots * min spacing
        leaf_spacing = self._NODE_R * 2.5
        tree_half_w = (2 ** (depth - 1)) * leaf_spacing

        top_y = 0.0
        self._assign_positions(0, 0, -tree_half_w, tree_half_w, top_y)

        parts: list[VMobject] = []

        # Edges first (drawn beneath nodes)
        for idx, pos in self._positions.items():
            parent_idx = (idx - 1) // 2
            if idx > 0 and parent_idx in self._positions:
                p_pos = self._positions[parent_idx]
                edge = Line(p_pos, pos, stroke_color=self.edge_color, stroke_width=1.5)
                self._edge_mobs[(parent_idx, idx)] = edge
                parts.append(edge)

        # Nodes
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

        # Name label (top-left)
        name_mob = Text(self.name + " =", font=self.font, color=self.data_color)
        name_mob.scale(0.4)
        parts.append(name_mob)

        group = VGroup(*parts)
        group.scale(self._SCALE)
        group.move_to(self.center)

        # Position the name label to the top-left of the tree
        name_mob.next_to(group, UL, buff=0.05)

        return group

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self, run_time: float = 1) -> None:
        self.scene.play(Create(self.mobject), run_time=run_time)

    def highlight_node(self, index: int, color: ManimColor = BLUE, run_time: float = 1) -> None:
        """Highlight the circle and label of the node at array `index`."""
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
        """Highlight the edge between parent and child nodes."""
        key = (parent_index, child_index)
        if key not in self._edge_mobs:
            return
        self.scene.play(
            self._edge_mobs[key].animate.set_stroke(color=color),
            run_time=run_time,
        )

    def disappear(self, run_time: float = 1) -> None:
        self.scene.play(FadeOut(self.mobject), run_time=run_time)


# ---------------------------------------------------------------------------
# MGraph
# ---------------------------------------------------------------------------

class MGraph:
    """Visualise a graph from an adjacency list dict.

    Nodes are arranged in a circle. Supports directed and undirected graphs.

    Example (undirected)
    --------------------
    MGraph("g", {0: [1, 2], 1: [2], 2: [3], 3: []}, directed=False, scene=self)

    Example (directed)
    ------------------
    MGraph("g", {0: [1], 1: [2], 2: [0]}, directed=True, scene=self)

    Parameters
    ----------
    name:     variable name label.
    adj:      adjacency dict  {node: [neighbour, ...], ...}.
    directed: if True, edges are drawn as arrows; otherwise as plain lines.
    scene:    the active Manim Scene.
    center:   where the centre of the graph is placed.
    radius:   radius of the circular node layout (unscaled).
    """

    _NODE_R: float = 0.3
    _SCALE: float = 0.85

    def __init__(
        self,
        name: str,
        adj: dict,
        scene: Scene,
        directed: bool = False,
        center: np.ndarray = ORIGIN,
        radius: float = 1.6,
        font: str = "CMU Serif",
        node_color: ManimColor = WHITE,
        edge_color: ManimColor = WHITE,
        data_color: ManimColor = WHITE,
    ) -> None:
        self.name = name
        self.adj = adj
        self.scene = scene
        self.directed = directed
        self.center = center
        self.radius = radius
        self.font = font
        self.node_color = node_color
        self.edge_color = edge_color
        self.data_color = data_color

        self.nodes: list = sorted(adj.keys())
        # node → (circle, label) VGroup
        self._node_mobs: dict = {}
        # node → position np.ndarray (unscaled local)
        self._positions: dict = {}
        # (u, v) → edge mobject (Line or Arrow); for undirected min(u,v) is key
        self._edge_mobs: dict[tuple, VMobject] = {}

        self.mobject = self._build()

    # ------------------------------------------------------------------
    # Build helpers
    # ------------------------------------------------------------------

    def _node_positions(self) -> dict:
        n = len(self.nodes)
        positions = {}
        for i, node in enumerate(self.nodes):
            angle = TAU * i / n - TAU / 4   # start from the top
            x = self.radius * np.cos(angle)
            y = self.radius * np.sin(angle)
            positions[node] = np.array([x, y, 0])
        return positions

    def _build(self) -> VGroup:
        self._positions = self._node_positions()
        parts: list[VMobject] = []

        # Track which undirected edges have been drawn
        drawn_undirected: set[frozenset] = set()

        # Edges
        for u, neighbours in self.adj.items():
            for v in neighbours:
                if v not in self._positions:
                    continue

                p_u = self._positions[u]
                p_v = self._positions[v]
                direction = p_v - p_u
                norm = np.linalg.norm(direction)
                if norm == 0:
                    continue
                unit = direction / norm

                if self.directed:
                    start = p_u + unit * self._NODE_R
                    end = p_v - unit * self._NODE_R
                    edge = Arrow(
                        start=start,
                        end=end,
                        buff=0,
                        stroke_width=1.5,
                        color=self.edge_color,
                        max_tip_length_to_length_ratio=0.2,
                    )
                    self._edge_mobs[(u, v)] = edge
                    parts.append(edge)
                else:
                    key = frozenset({u, v})
                    if key in drawn_undirected:
                        continue
                    drawn_undirected.add(key)
                    start = p_u + unit * self._NODE_R
                    end = p_v - unit * self._NODE_R
                    edge = Line(
                        start=start,
                        end=end,
                        stroke_color=self.edge_color,
                        stroke_width=1.5,
                    )
                    self._edge_mobs[(min(u, v), max(u, v))] = edge
                    parts.append(edge)

        # Nodes (drawn on top of edges)
        for node in self.nodes:
            pos = self._positions[node]
            circle = Circle(
                radius=self._NODE_R,
                stroke_color=self.node_color,
                fill_color=BLACK,
                fill_opacity=1,
                stroke_width=1.5,
            )
            circle.move_to(pos)
            label = Text(str(node), font=self.font, color=self.data_color)
            label.scale_to_fit_width(self._NODE_R * 1.1)
            label.move_to(pos)
            node_mob = VGroup(circle, label)
            self._node_mobs[node] = node_mob
            parts.append(node_mob)

        # Name label
        name_mob = Text(self.name + " =", font=self.font, color=self.data_color)
        name_mob.scale(0.4)
        parts.append(name_mob)

        group = VGroup(*parts)
        group.scale(self._SCALE)
        group.move_to(self.center)
        name_mob.next_to(group, UL, buff=0.05)

        return group

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self, run_time: float = 1) -> None:
        self.scene.play(Create(self.mobject), run_time=run_time)

    def highlight_node(self, node, color: ManimColor = BLUE, run_time: float = 1) -> None:
        """Highlight a node's circle and label."""
        if node not in self._node_mobs:
            return
        circle, label = self._node_mobs[node]
        self.scene.play(
            circle.animate.set_stroke(color=color),
            label.animate.set_color(color=color),
            run_time=run_time,
        )

    def highlight_edge(self, u, v, color: ManimColor = BLUE, run_time: float = 1) -> None:
        """Highlight the edge between nodes u and v.

        For undirected graphs pass nodes in either order.
        For directed graphs, (u, v) must match the direction of the edge.
        """
        key: tuple
        if self.directed:
            key = (u, v)
        else:
            key = (min(u, v), max(u, v))

        if key not in self._edge_mobs:
            return
        self.scene.play(
            self._edge_mobs[key].animate.set_color(color=color),
            run_time=run_time,
        )

    def disappear(self, run_time: float = 1) -> None:
        self.scene.play(FadeOut(self.mobject), run_time=run_time)
