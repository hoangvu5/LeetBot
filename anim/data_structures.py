from manim import *
import numpy as np

class MVariable:
    def __init__(self, name, variable, scene, center=ORIGIN, font="CMU Serif", data_color=WHITE):
        self.name = name
        self.variable = variable
        self.center = center
        self.font = font
        self.data_color = data_color
        self.scene = scene

        self.mobject = Text(name + " = " + str(variable), font=self.font)
        self.mobject.scale(0.5)
        self.mobject.move_to(self.center)

    def run(self, run_time=1):
        self.scene.play(Create(self.mobject), run_time=run_time)

    def highlight_variable(self, color=BLUE, run_time=1):
        self.scene.play(self.mobject.animate.set_color(color=color), run_time=run_time)

    def disappear(self, run_time=1):
        self.scene.play(FadeOut(self.mobject), run_time=run_time)

class MElement:
    def __init__(self, data, index, center=ORIGIN, width=0.4,
        font="CMU Serif", stroke_color=WHITE, data_color=WHITE, show_index=True):
        self.data = data
        self.index = index
        self.center = center
        self.width = width
        self.font = font
        self.stroke_color = stroke_color
        self.data_color = data_color
        self.show_index = show_index

        self.mdata = Text(str(data), color=self.data_color, font=self.font)
        self.mdata.scale(1.0)
        self.mdata.move_to(self.center)

        self.mrectangle = RoundedRectangle(
            height=self.width,
            width=self.width,
            stroke_color=self.stroke_color,
            fill_opacity=0,
            stroke_width=1,
            corner_radius=0.2
        )
        self.mrectangle.scale(1.0)
        self.mrectangle.move_to(self.center)

        self.mindex = Text(str(self.index), color=self.data_color, font=self.font)
        self.mindex.scale(0.5)
        self.mindex.next_to(self.mrectangle, UP, buff=0.2)

        self.mobject = VGroup(self.mdata, self.mrectangle, self.mindex)

class MArray:
    def __init__(self, name, array, scene, center=ORIGIN, width=1, 
            font="CMU Serif", margin=0.1, stroke_color=WHITE, data_color=WHITE, show_index=True):
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
        self.mtitle.scale(1.0)

        # 3 * margin between title and array
        self.count = len(array)
        self.total_width = (self.count * self.width) + ((self.count + 2) * self.margin) + self.mtitle.width
        
        self.mtitle.move_to(np.array([self.center[0] - self.total_width / 2 + self.mtitle.width / 2, self.center[1], 0]))

        self.marray = []

        # Render the array so that it lies at center
        start_x = self.center[0] - self.total_width / 2 + self.mtitle.width + self.width / 2 + self.margin * 3
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
                show_index=self.show_index
            )
            self.marray.append(melement)

        self.mobject = VGroup(self.mtitle, *[melement.mobject for melement in self.marray])
        self.mobject.scale(0.5)
    
    def run(self, run_time=1):
        self.scene.play(Create(self.mobject), run_time=run_time)

    def highlight_element(self, index, color=BLUE, run_time=1):
        self.scene.play(
            self.marray[index].mrectangle.animate.set_stroke(color=color),
            self.marray[index].mdata.animate.set_color(color=color),
            run_time=run_time
        )

    def highlight_range(self, start, end, color=BLUE, run_time=1):
        animations = [
            self.marray[i].mrectangle.animate.set_stroke(color=color)
            for i in range(start, end + 1)
        ] + [
            self.marray[i].mdata.animate.set_color(color=color)
            for i in range(start, end + 1)
        ]
        self.scene.play(*animations, run_time=run_time)

    def highlight_elements(self, indices, color=BLUE, run_time=1):
        animations = [
            self.marray[i].mrectangle.animate.set_stroke(color=color)
            for i in indices
        ] + [
            self.marray[i].mdata.animate.set_color(color=color)
            for i in indices
        ]
        self.scene.play(*animations, run_time=run_time)

class MTitle:
    def __init__(self, title, subtitle, scene, center=ORIGIN, color=WHITE):
        self.title = title
        self.subtitle = subtitle
        self.center = center
        self.color = color
        self.scene = scene

        self.mtitle = Text(str(title), color=self.color)
        self.mtitle.scale(1.0)
        self.mtitle.move_to(self.center)

        msubtitle_color = {"Easy": "#46c6c2", "Medium": "#fac31d", "Hard": "#f8615c"}.get(self.subtitle, "#ffffff")
        self.msubtitle = Text(
            "Difficulty: " + self.subtitle,                   
            t2c={self.subtitle:hex_to_rgb(msubtitle_color)}, 
        )
        self.msubtitle.scale(0.5)
        self.msubtitle.move_to(self.center + DOWN * 0.75)

    def run(self, run_time=1):
        self.scene.play(
            Create(self.mtitle),
            Create(self.msubtitle),
            run_time=0.25
        )
        self.scene.wait(run_time - 0.5)
        self.scene.play(
            self.mtitle.animate.move_to(UP * 3.25).scale(0.25),
            self.msubtitle.animate.move_to(UP * 2.90).scale(0.5),
            run_time=0.25
        )

class MMap:
    def __init__(self, name, map, scene, center=ORIGIN, width=1, 
        font="CMU Serif", margin=0.1, stroke_color=WHITE, data_color=WHITE):
        self.name = name
        self.map = map
        self.scene = scene
        self.center = center
        self.width = width
        self.font = font
        self.margin = margin
        self.stroke_color = stroke_color
        self.data_color = data_color

        map_str = self.name + " = {" + ", ".join([f"{k}: {v}" for k, v in self.map.items()]) + "}"
        self.mobject = Text(map_str, font=self.font)
        self.mobject.scale(0.5)
        self.mobject.move_to(self.center)

    def run(self, run_time=1):
        self.scene.play(Create(self.mobject), run_time=run_time)

    def insert_element(self, key, value, run_time=1):
        old_mobject = self.mobject
        self.map[key] = value
        map_str = self.name + " = {" + ", ".join([f"{k}: {v}" for k, v in self.map.items()]) + "}"
        self.mobject = Text(map_str, font=self.font)
        self.mobject.scale(0.5)
        self.mobject.move_to(old_mobject.get_center())
        self.scene.play(ReplacementTransform(old_mobject, self.mobject), run_time=run_time)
        

    def remove_element(self, key, run_time=1):
        old_mobject = self.mobject
        del self.map[key]
        map_str = "{" + ", ".join([f"{k}: {v}" for k, v in self.map.items()]) + "}"
        self.mobject = Text(map_str, font=self.font)
        self.mobject.scale(0.5)
        self.mobject.move_to(old_mobject.get_center())
        self.scene.play(ReplacementTransform(old_mobject, self.mobject), run_time=run_time)

    def highlight_element(self, key, color=BLUE, run_time=1):
        if key not in self.map:
            return

        old_mobject = self.mobject
        map_str = self.name + " = {" + ", ".join([f"{k}: {v}" for k, v in self.map.items()]) + "}"
        self.mobject = Text(map_str, font=self.font, t2c={str(key): color, str(self.map[key]): color})
        self.mobject.scale(0.5)
        self.mobject.move_to(old_mobject.get_center())
        self.scene.play(ReplacementTransform(old_mobject, self.mobject), run_time=run_time)

class MText:
    def __init__(self, text, scene, center=ORIGIN, font="CMU Serif", data_color=WHITE, wraparound=True):
        self.text = text
        self.scene = scene
        self.center = center
        self.font = font
        self.data_color = data_color
        self.wraparound = wraparound

        self.mobject = Text(str(self.text), font=self.font, color=self.data_color)
        self.mobject.scale(0.45)
        self.mobject.move_to(self.center)

    def run(self, run_time=1):
        self.scene.play(Create(self.mobject), run_time=run_time)

    def edit(self, new_text, run_time=1):
        old_mobject = self.mobject
        self.text = new_text
        self.mobject = Text(str(self.text), font=self.font, color=self.data_color)
        self.mobject.scale(0.5)
        self.mobject.move_to(old_mobject.get_center())
        self.scene.play(ReplacementTransform(old_mobject, self.mobject), run_time=run_time)

    def disappear(self, run_time=1):
        self.scene.play(FadeOut(self.mobject), run_time=run_time)

class MStack:
    def __init__(self, name, stack, scene, center=ORIGIN, width=1, 
            font="CMU Serif", margin=0.1, stroke_color=WHITE, data_color=WHITE):
        self.name = name + " = "
        self.stack = stack
        self.center = center
        self.width = width
        self.font = font
        self.margin = margin # from border
        self.stroke_color = stroke_color
        self.data_color = data_color
        self.scene = scene

        self.mtitle = Text(str(self.name), color=self.data_color, font=self.font)
        self.mtitle.scale(1.0)
        self.mtitle.move_to(np.array([self.center[0] - config["frame_width"] / 2 + 3 * self.margin + self.mtitle.width / 2, self.center[1], 0]))

        self.top_center = np.array([self.center[0] - config["frame_width"] / 2 + 6 * self.margin + self.mtitle.width, self.center[1], 0])
        self.count = len(stack)
        self.total_width = config["frame_width"] - 8 * self.margin - self.mtitle.width

        # Create two horizontal lines
        left_line_start = np.array([self.center[0] - config["frame_width"] / 2 + 5 * self.margin + self.mtitle.width, self.center[1] + self.width + self.margin, 0])
        left_line_end = np.array([self.center[0] + config["frame_width"] / 2 - 3 * self.margin, self.center[1] + self.width + self.margin, 0])
        right_line_start = np.array([self.center[0] - config["frame_width"] / 2 + 5 * self.margin + self.mtitle.width, self.center[1] - self.width - self.margin, 0])
        right_line_end = np.array([self.center[0] + config["frame_width"] / 2 - 3 * self.margin, self.center[1] - self.width - self.margin, 0])

        self.left_line = Line(left_line_start, left_line_end, stroke_color=self.stroke_color)
        self.right_line = Line(right_line_start, right_line_end, stroke_color=self.stroke_color)

        # Create a vertical line connecting the left points of the two horizontal lines
        vertical_line_start = left_line_start
        vertical_line_end = right_line_start
        self.vertical_line = Line(vertical_line_start, vertical_line_end, stroke_color=self.stroke_color)

        # Assign self.mbox to the VGroup of the three lines
        self.mbox = VGroup(self.left_line, self.right_line, self.vertical_line)
        self.mstack = []

        # Render the stack so that it lies at center
        for idx, value in enumerate(self.stack):
            melement = MElement(
                data=value, 
                index=idx, 
                center=self.top_center,
                width=self.width,
                font=self.font,
                stroke_color=self.stroke_color,
                data_color=self.data_color,
                show_index=False
            )
            self.mstack.append(melement)
            self.top_center[0] += self.width + self.margin

        self.mobject = VGroup(self.mtitle, self.mbox, *[melement.mobject for melement in self.mstack])
        self.mobject.scale(0.5)
    
    def run(self, run_time=1):
        self.scene.play(Create(self.mobject), run_time=run_time)

    def highlight_top(self, color=BLUE, run_time=1):
        if not self.mstack:
            return
        top_element = self.mstack[-1]
        self.scene.play(
            top_element.mrectangle.animate.set_stroke(color=color),
            top_element.mdata.animate.set_color(color=color),
            run_time=run_time
        )

    def push(self, value, run_time=1):
        new_center = self.top_center.copy()
        melement = MElement(
            data=value,
            index=len(self.mstack),
            center=new_center,
            width=self.width,
            font=self.font,
            stroke_color=self.stroke_color,
            data_color=self.data_color,
            show_index=False
        )
        self.mstack.append(melement)
        self.top_center[0] += self.width + self.margin
        self.mobject.add(melement.mobject)
        self.scene.play(FadeIn(melement.mobject), run_time=run_time)

    def pop(self, run_time=1):
        if not self.mstack:
            return -1
        top_element = self.mstack.pop()
        self.top_center[0] -= self.width + self.margin
        self.scene.play(FadeOut(top_element.mobject), run_time=run_time)
        return top_element.data

    def top(self):
        if not self.mstack:
            return -1
        return self.mstack[-1].data
        
        
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16) / 255
    g = int(hex_color[2:4], 16) / 255
    b = int(hex_color[4:6], 16) / 255
    return ManimColor([r, g, b])