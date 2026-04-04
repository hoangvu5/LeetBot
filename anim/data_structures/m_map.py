from __future__ import annotations
from manim import *
import numpy as np


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
