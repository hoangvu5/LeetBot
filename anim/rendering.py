from manim import *
import numpy as np
from data_structures import *

class MProblem(Scene):
    def construct(self):
        coor = ORIGIN + UP * 1.5
        time_elapsed = 0.0

        title = MTitle("Two Sum", "Easy", scene=self)
        title.run(run_time=1)
        time_elapsed += 1.0

        arr = MArray("nums", [2, 7, 11, 15], scene=self, center=coor)
        arr.run(run_time=1)
        time_elapsed += 1.0
        coor[1] -= 1.3

        target = MVariable("target", 9, scene=self, center=coor)
        target.run(run_time=1)
        time_elapsed += 1.0
        coor[1] -= 1.0

        if 4.0 - time_elapsed > 0:
            self.wait(4.0 - time_elapsed)
            time_elapsed = 4.0

        if 6.84 - time_elapsed > 0:
            self.wait(6.84 - time_elapsed)
            time_elapsed = 6.84

        arr.highlight_elements([0, 1, 2, 3], color=BLUE, run_time=1)
        time_elapsed += 1.0

        if 11.62 - time_elapsed > 0:
            self.wait(11.62 - time_elapsed)
            time_elapsed = 11.62

        target.highlight_variable(color=YELLOW, run_time=1)
        time_elapsed += 1.0

        if 15.6 - time_elapsed > 0:
            self.wait(15.6 - time_elapsed)
            time_elapsed = 15.6

        arr.highlight_elements([0, 1], color=GREEN, run_time=1)
        time_elapsed += 1.0

        if 20.96 - time_elapsed > 0:
            self.wait(20.96 - time_elapsed)
            time_elapsed = 20.96

        ans = MText("[0, 1]", scene=self, center=coor)
        ans.run(run_time=1)
        time_elapsed += 1.0
        coor[1] -= 1.0

        if 25.66 - time_elapsed > 0:
            self.wait(25.66 - time_elapsed)
            time_elapsed = 25.66

        ans.disappear(run_time=0.8)
        time_elapsed += 0.8
        coor[1] += 1.0

        target.disappear(run_time=0.8)
        time_elapsed += 0.8
        coor[1] += 1.0

        if 27.74 - time_elapsed > 0:
            self.wait(27.74 - time_elapsed)
            time_elapsed = 27.74

        mp = MMap("seen", {}, scene=self, center=coor)
        mp.run(run_time=1)
        time_elapsed += 1.0
        coor[1] -= 1.0

        if 30.08 - time_elapsed > 0:
            self.wait(30.08 - time_elapsed)
            time_elapsed = 30.08

        arr.highlight_element(0, color=YELLOW, run_time=0.8)
        time_elapsed += 0.8
        mp.insert_element(2, 0, run_time=0.8)
        time_elapsed += 0.8

        if 34.32 - time_elapsed > 0:
            self.wait(34.32 - time_elapsed)
            time_elapsed = 34.32

        arr.highlight_element(1, color=YELLOW, run_time=0.8)
        time_elapsed += 0.8
        mp.highlight_element(2, color=BLUE, run_time=0.8)
        time_elapsed += 0.8

        if 36.92 - time_elapsed > 0:
            self.wait(36.92 - time_elapsed)
            time_elapsed = 36.92

        arr.highlight_elements([0, 1], color=GREEN, run_time=1)
        time_elapsed += 1.0
        mp.highlight_element(2, color=GREEN, run_time=0.8)
        time_elapsed += 0.8

        if 41.62 - time_elapsed > 0:
            self.wait(41.62 - time_elapsed)
            time_elapsed = 41.62

        note = MText("9 - 7 = 2", scene=self, center=coor)
        note.run(run_time=0.8)
        time_elapsed += 0.8
        coor[1] -= 1.0

        if 44.54 - time_elapsed > 0:
            self.wait(44.54 - time_elapsed)
            time_elapsed = 44.54

        note.edit("found complement", run_time=0.8)
        time_elapsed += 0.8

        if 45.3 - time_elapsed > 0:
            self.wait(45.3 - time_elapsed)
