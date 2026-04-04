from __future__ import annotations
from manim import *
import numpy as np


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
        self._node_mobs: dict = {}
        self._positions: dict = {}
        self._edge_mobs: dict[tuple, VMobject] = {}

        self.mobject = self._build()

    def _node_positions(self) -> dict:
        n = len(self.nodes)
        positions = {}
        for i, node in enumerate(self.nodes):
            angle = TAU * i / n - TAU / 4
            x = self.radius * np.cos(angle)
            y = self.radius * np.sin(angle)
            positions[node] = np.array([x, y, 0])
        return positions

    def _build(self) -> VGroup:
        self._positions = self._node_positions()
        parts: list[VMobject] = []
        drawn_undirected: set[frozenset] = set()

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
                        start=start, end=end, buff=0,
                        stroke_width=1.5, color=self.edge_color,
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
                    edge = Line(start=start, end=end, stroke_color=self.edge_color, stroke_width=1.5)
                    self._edge_mobs[(min(u, v), max(u, v))] = edge
                    parts.append(edge)

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

    def highlight_node(self, node, color: ManimColor = BLUE, run_time: float = 1) -> None:
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
