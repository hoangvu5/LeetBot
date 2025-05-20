from manim import *
import numpy as np
from data_structures import *

class MProblem(Scene):    
    def construct(self):
        coor = ORIGIN + UP * 2.05

        # Display the title
        title = MTitle("Separate Black and White Balls", "Medium", scene=self) # added scene=self
        title.run(run_time=1)
        self.wait(3.3399999141693115 - 1)

        # Create and display the array
        balls = MArray("s", [1, 0, 1], scene=self, center=coor)
        balls.run(run_time=1)
        self.wait(31.5 - 3.3399999141693115 - 1)
        coor[1] -= 0.5

        # Highlight the elements to be swapped
        balls.highlight_elements([0, 1], color=BLUE, run_time=1)
        self.wait(42.36000061035156 - 31.5 - 1)

        # Swap the elements
        balls.array[0], balls.array[1] = balls.array[1], balls.array[0]
        balls.run(run_time=1)
        self.wait(49.91999816894531 - 42.36000061035156 - 1)

        # Explanation of the swap
        explanation = MText("Swap index 0 and 1 to get 011", scene=self, center=coor)
        explanation.run(run_time=1)
        self.wait(57.790000915527344 - 49.91999816894531 - 1)
        coor[1] -= 0.5

        # Display the minimum steps
        min_steps = MVariable("Minimum Steps", 1, scene=self, center=coor)
        min_steps.run(run_time=1)
        self.wait(68.18000030517578 - 57.790000915527344 - 1)
        coor[1] -= 0.5

        # Thought process explanation
        thought_process = MText("Count black balls on left needing swap", scene=self, center=coor)
        thought_process.run(run_time=1)
        self.wait(85.44000244140625 - 68.18000030517578 - 1)
        coor[1] -= 0.5

        # Clean up
        explanation.disappear(run_time=1)
        min_steps.disappear(run_time=1)
        thought_process.disappear(run_time=1)
        balls.highlight_elements([0, 1], color=WHITE, run_time=1)
        self.wait(1)
        coor[1] += 1.5