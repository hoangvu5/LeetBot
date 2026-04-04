from manim import *
import numpy as np
from data_structures import *

class MProblem(Scene):
    def construct(self):
        coor = ORIGIN + UP * 1.5
        time_elapsed = 0.0

        title = MTitle("Two Sum", "Easy", scene=self)
        title.run(run_time=1.2)
        time_elapsed += 1.2

        if 4.0 - time_elapsed > 0:
            self.wait(4.0 - time_elapsed)
            time_elapsed = 4.0

        arr = MArray("nums", [2, 7, 11, 15], scene=self, center=coor)
        arr.run(run_time=1.2)
        time_elapsed += 1.2
        coor[1] -= 1.3

        if 6.84 - time_elapsed > 0:
            self.wait(6.84 - time_elapsed)
            time_elapsed = 6.84

        target = MVariable("target", 9, scene=self, center=coor)
        target.run(run_time=1.0)
        time_elapsed += 1.0
        coor[1] -= 1.0

        if 11.62 - time_elapsed > 0:
            self.wait(11.62 - time_elapsed)
            time_elapsed = 11.62

        arr.highlight_element(0, color=YELLOW, run_time=0.8)
        time_elapsed += 0.8
        arr.highlight_element(1, color=YELLOW, run_time=0.8)
        time_elapsed += 0.8

        if 15.6 - time_elapsed > 0:
            self.wait(15.6 - time_elapsed)
            time_elapsed = 15.6

        pair = MText("2 + 7 = 9", scene=self, center=coor)
        pair.run(run_time=1.0)
        time_elapsed += 1.0
        coor[1] -= 1.0

        if 20.96 - time_elapsed > 0:
            self.wait(20.96 - time_elapsed)
            time_elapsed = 20.96

        pair.edit("output: [0, 1]", run_time=1.0)
        time_elapsed += 1.0

        if 25.66 - time_elapsed > 0:
            self.wait(25.66 - time_elapsed)
            time_elapsed = 25.66

        pair.disappear(run_time=0.6)
        time_elapsed += 0.6
        coor[1] += 1.0

        target.disappear(run_time=0.6)
        time_elapsed += 0.6
        coor[1] += 1.0

        if 27.74 - time_elapsed > 0:
            self.wait(27.74 - time_elapsed)
            time_elapsed = 27.74

        mp = MHashMap("seen", scene=self, center=coor)
        mp.run(run_time=1.0)
        time_elapsed += 1.0
        coor[1] -= 1.0

        if 30.08 - time_elapsed > 0:
            self.wait(30.08 - time_elapsed)
            time_elapsed = 30.08

        arr.highlight_element(0, color=BLUE, run_time=0.7)
        time_elapsed += 0.7
        note = MText("need 7", scene=self, center=coor)
        note.run(run_time=0.7)
        time_elapsed += 0.7
        coor[1] -= 1.0

        if 34.32 - time_elapsed > 0:
            self.wait(34.32 - time_elapsed)
            time_elapsed = 34.32

        mp.insert_element(2, 0, below_mobs=[note.mobject], run_time=1.0)
        time_elapsed += 1.0

        if 36.92 - time_elapsed > 0:
            self.wait(36.92 - time_elapsed)
            time_elapsed = 36.92

        arr.highlight_element(1, color=GREEN, run_time=0.7)
        time_elapsed += 0.7
        note.edit("need 2", run_time=0.7)
        time_elapsed += 0.7
        mp.highlight_element(2, color=GREEN, run_time=0.8)
        time_elapsed += 0.8

        if 41.62 - time_elapsed > 0:
            self.wait(41.62 - time_elapsed)
            time_elapsed = 41.62

        note.edit("found pair", run_time=0.8)
        time_elapsed += 0.8

        if 44.54 - time_elapsed > 0:
            self.wait(44.54 - time_elapsed)
            time_elapsed = 44.54

        note.edit("[0, 1]", run_time=0.76)
        time_elapsed += 0.76

        if 45.3 - time_elapsed > 0:
            self.wait(45.3 - time_elapsed)
            time_elapsed = 45.3

        self.wait(2)
