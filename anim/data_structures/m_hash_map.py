from __future__ import annotations
from manim import *
import numpy as np


class MHashMap:
    """Visualise a hash map as a vertical list of key → value rows flanked by curly braces.

    Layout (after internal scaling):
        name = { "key1" → "val1" }
               { "key2" → "val2" }

    The structure expands downward as rows are inserted.  Pass ``below_mobs``
    to ``insert_element`` / ``remove_element`` to shift other on-screen
    objects in sync with the expansion.

    Parameters
    ----------
    name   : variable name shown as a label to the left.
    scene  : the active Manim Scene.
    center : where the name label is placed.
    """

    _SCALE: float      = 0.45
    _ROW_BUFF: float   = 0.12
    _BRACE_PAD: float  = 0.15
    _BRACE_BUFF: float = 0.08

    def __init__(
        self,
        name: str,
        scene: Scene,
        center: np.ndarray = ORIGIN,
        font: str = "CMU Serif",
        data_color: ManimColor = WHITE,
    ) -> None:
        self.name       = name
        self.scene      = scene
        self.center     = np.array(center, dtype=float)
        self.font       = font
        self.data_color = data_color

        self.data: dict = {}
        self._rows: dict = {}
        self._left_brace:  Text | None = None
        self._right_brace: Text | None = None

        self._name_mob = Text(name + " =", font=font, color=data_color)
        self._name_mob.scale(self._SCALE)
        self._name_mob.move_to(self.center)

        self.mobject = VGroup(self._name_mob)

    def _fmt(self, val) -> str:
        return f'"{val}"' if isinstance(val, str) else str(val)

    def _make_row(self, key, value) -> Text:
        t = Text(
            f"{self._fmt(key)} \u2192 {self._fmt(value)}",
            font=self.font,
            color=self.data_color,
        )
        t.scale(self._SCALE)
        return t

    def _make_brace(self, char: str, rows_vg: VGroup) -> Text:
        b = Text(char, font=self.font, color=self.data_color)
        b.scale_to_fit_height(rows_vg.height + self._BRACE_PAD)
        return b

    def _rows_vgroup(self) -> VGroup:
        return VGroup(*[self._rows[k] for k in self.data])

    def _refresh_mobject(self) -> None:
        if self._left_brace is not None:
            self.mobject = VGroup(
                self._name_mob,
                self._rows_vgroup(),
                self._left_brace,
                self._right_brace,
            )
        else:
            self.mobject = VGroup(self._name_mob)

    def run(self, run_time: float = 1) -> None:
        self.scene.play(Create(self._name_mob), run_time=run_time)

    def insert_element(
        self,
        key,
        value,
        below_mobs=None,
        run_time: float = 1,
    ) -> None:
        """Add a key→value row, expanding the structure downward.

        Parameters
        ----------
        below_mobs : mobject or list of mobjects to shift DOWN by the row height.
        """
        self.data[key] = value
        new_row = self._make_row(key, value)

        if not self._rows:
            new_row.next_to(self._name_mob, RIGHT, buff=0.5)
            new_row.align_to(self._name_mob, UP)
        else:
            last_row = list(self._rows.values())[-1]
            new_row.next_to(last_row, DOWN, buff=self._ROW_BUFF)
            new_row.align_to(last_row, LEFT)

        row_shift = new_row.height + self._ROW_BUFF

        self._rows[key] = new_row
        rv = self._rows_vgroup()

        new_left = self._make_brace("{", rv)
        new_left.next_to(rv, LEFT, buff=self._BRACE_BUFF)
        new_right = self._make_brace("}", rv)
        new_right.next_to(rv, RIGHT, buff=self._BRACE_BUFF)

        animations: list = [FadeIn(new_row)]
        if self._left_brace is None:
            animations += [FadeIn(new_left), FadeIn(new_right)]
        else:
            animations += [
                ReplacementTransform(self._left_brace, new_left),
                ReplacementTransform(self._right_brace, new_right),
            ]

        mobs = below_mobs if isinstance(below_mobs, (list, tuple)) else ([below_mobs] if below_mobs else [])
        for mob in mobs:
            animations.append(mob.animate.shift(DOWN * row_shift))

        self.scene.play(*animations, run_time=run_time)

        self._left_brace  = new_left
        self._right_brace = new_right
        self._refresh_mobject()

    def remove_element(
        self,
        key,
        below_mobs=None,
        run_time: float = 1,
    ) -> None:
        """Remove the row for *key*, contracting the structure upward.

        Parameters
        ----------
        below_mobs : mobject or list of mobjects to shift UP by the row height.
        """
        if key not in self._rows:
            return

        row_to_remove = self._rows.pop(key)
        del self.data[key]
        row_shift = row_to_remove.height + self._ROW_BUFF

        removed_y = row_to_remove.get_center()[1]
        animations: list = [FadeOut(row_to_remove)]
        for k in self.data:
            if self._rows[k].get_center()[1] < removed_y:
                animations.append(self._rows[k].animate.shift(UP * row_shift))

        mobs = below_mobs if isinstance(below_mobs, (list, tuple)) else ([below_mobs] if below_mobs else [])
        for mob in mobs:
            animations.append(mob.animate.shift(UP * row_shift))

        if self._left_brace:
            animations += [FadeOut(self._left_brace), FadeOut(self._right_brace)]

        self.scene.play(*animations, run_time=run_time)
        self._left_brace  = None
        self._right_brace = None

        if self.data:
            rv = self._rows_vgroup()
            new_left = self._make_brace("{", rv)
            new_left.next_to(rv, LEFT, buff=self._BRACE_BUFF)
            new_right = self._make_brace("}", rv)
            new_right.next_to(rv, RIGHT, buff=self._BRACE_BUFF)
            self.scene.play(FadeIn(new_left), FadeIn(new_right), run_time=0.3)
            self._left_brace  = new_left
            self._right_brace = new_right

        self._refresh_mobject()

    def highlight_element(
        self,
        key,
        color: ManimColor = BLUE,
        run_time: float = 1,
    ) -> None:
        if key not in self._rows:
            return
        self.scene.play(self._rows[key].animate.set_color(color), run_time=run_time)

    def disappear(self, run_time: float = 1) -> None:
        self.scene.play(FadeOut(self.mobject), run_time=run_time)
