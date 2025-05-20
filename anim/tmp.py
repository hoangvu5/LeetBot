from manim import *
import random

from collections import deque

class GraphNode:
    def __init__(self, data, center=ORIGIN, radius=0.5, neighbors=[], scale=1):
        self.char = data
        self.data = Text(str(data))
        self.data.scale(scale)
        self.neighbors = []
        self.center = center
        self.radius = radius
        self.circle = Circle(radius=radius)
        self.circle.move_to(center)
        self.data.move_to(center)
        self.drawn = False
        self.marked = False
        self.edges = []
        self.prev = None

    def connect(self, other):
        line_center = Line(self.center, other.center)
        unit_vector = line_center.get_unit_vector()
        start, end = line_center.get_start_and_end()
        new_start = start + unit_vector * self.radius
        new_end = end - unit_vector * self.radius
        line = Line(new_start, new_end)
        self.neighbors.append(other)
        other.neighbors.append(self)
        self.edges.append(line)
        other.edges.append(line)
        return line

    def connect_arrow(self, other):
        line_center = Line(self.center, other.center)
        unit_vector = line_center.get_unit_vector()
        start, end = line_center.get_start_and_end()
        new_start = start + unit_vector * self.radius / 2
        new_end = end - unit_vector * self.radius / 2
        arrow = Arrow(new_start, new_end)
        arrow.buff = self.radius / 2
        arrow.unit_vector = unit_vector
        self.neighbors.append(other)
        self.edges.append(arrow)
        return arrow

    def connect_curve(self, counter_clock_adj_self, other, clockwise_adj_other, angle=TAU / 4):
        line_self = Line(counter_clock_adj_self.circle.get_center(), self.circle.get_center())
        unit_vector_self = line_self.get_unit_vector()
        line_other = Line(clockwise_adj_other.circle.get_center(), other.circle.get_center())
        unit_vector_other = line_other.get_unit_vector()
        curve_start = self.circle.get_center() + unit_vector_self * self.radius
        curve_end = other.circle.get_center() + unit_vector_other * self.radius
        line = ArcBetweenPoints(curve_start, curve_end, angle=angle)
        self.neighbors.append(other)
        other.neighbors.append(self)
        self.edges.append(line)
        other.edges.append(line)

    def make_mobject(self, show_data=True):
        if show_data:
            return VGroup(self.circle, self.data)
        return self.circle

    def __repr__(self):
        return 'GraphNode({0})'.format(self.char)

    def __str__(self):
        return 'GraphNode({0})'.format(self.char)
    
# TODO: Do DFS on that tree

class Tree:
    def __init__(self, name, array, center=ORIGIN, scale=1.0,
        radius=0.4, node_color=DARK_BLUE, stroke_color=BLUE, 
        data_color=WHITE, edge_color=GRAY, show_data=True):
        self.array = array
        self.name = name
        self.center = center
        self.scale = scale
        self.objects = []
        
        self.count = 0

        self.title = Text(str(name))
        self.nodes = []
        self.edges = {}

        self.radius = radius
        self.node_color = node_color
        self.stroke_color = stroke_color
        self.data_color = data_color
        self.edge_color = edge_color
        self.show_data = show_data

        self.interactive_mode = False
    
    # insert GraphNode in tree, Line in edges
    def build(self):
        self.title.scale(self.scale)
        self.title.move_to(self.center + LEFT * 1.5)

        queue = deque()
        i = 0
        for _, value in enumerate(self.array):
            if value is None:
                if queue:
                    queue.popleft()
                continue
            
            node = GraphNode(value, radius=self.radius, scale=self.scale)
            self.objects.append(node)
            if queue:
                parent, direction, j = queue.popleft()
                shift = LEFT * 1 + DOWN * 1 if direction == 'left' else RIGHT * 1 + DOWN * 1
                node.center = parent.center + shift
                self.edges[(j, i)] = parent.connect(node)
            else:
                node.center = self.center

            # Edit the style of the node
            node.circle.move_to(node.center)
            node.circle.set_fill(color=self.node_color, opacity=0.5)
            node.circle.set_stroke(color=self.stroke_color)
            node.data.move_to(node.center)
            node.data.set_color(color=self.data_color)

            self.nodes.append(node.make_mobject(self.show_data))
            queue.append((node, 'left', i))
            queue.append((node, 'right', i))
            i += 1
        
        self.count = i

    def make_mobject(self):
        return VGroup(VGroup(*self.nodes), VGroup(*self.edges.values()))
    
    def show_traversal(self, full_order, wait_times, scale_factor=1, run_time=1):
        i = 0
        angle = 180
        all_highlights = []
        for element in full_order:
            if isinstance(element, int):
                surround_circle = self.highlight_node(element, 
                    start_angle=angle/360 * TAU, scale_factor=scale_factor, run_time=run_time)
                all_highlights.append(surround_circle)
            else:
                last_edge = self.sharpie_edge(element[0], element[1], 
                    scale_factor=scale_factor, run_time=run_time)
                angle = self.find_angle_of_intersection(element[0].circle.get_center(), element[1].circle.get_center())
                all_highlights.append(last_edge)
            self.wait(wait_times[i])
            i += 1
        return all_highlights
    
    def highlight_node(self, index, color=GREEN, 
        start_angle=TAU/2, scale_factor=1, animate=True, run_time=1):
        node = self.objects[index]
        surround_circle = Circle(radius=node.circle.radius * scale_factor)
        surround_circle.move_to(node.circle.get_center())
        surround_circle.set_stroke(width=8 * scale_factor)
        surround_circle.set_color(color)
        surround_circle.set_fill(opacity=0)
        if animate:
            self.play(
                Create(surround_circle),
                run_time=run_time
            )
        return surround_circle
    
    def sharpie_edge(self, u, v, color=GREEN, 
        scale_factor=1, animate=True, run_time=1):
        switch = False
        if u > v:
            edge = self.edges[(v, u)]
            switch = True
        else:
            edge = self.edges[(u, v)]
        
        if not switch:
            line = Line(edge.get_start(), edge.get_end())
        else:
            line = Line(edge.get_end(), edge.get_start())
        line.set_stroke(width=16 * scale_factor)
        line.set_color(color)
        if animate:
            self.play(
                Create(line),
                run_time=run_time
            )
        return line
    
    def find_angle_of_intersection(self, last_point, node_index):
        node = self.nodes[node_index]
        distances = []
        for angle in range(360):
            respective_line = Line(node.circle.get_center(), 
                node.circle.get_center() + RIGHT * node.circle.radius)
            rotate_angle = angle / 360 * TAU
            respective_line.rotate(rotate_angle, about_point=node.circle.get_center())
            end_point = respective_line.get_end()
            distance = np.linalg.norm(end_point - last_point)
            distances.append(distance)
        return np.argmin(np.array(distances))

#  1
#   2
#  3 4
# 5
class Introduction(Scene):
    def construct(self):
        array = [1, None, 2, 3, 4, 5]
        tree = Tree('array', array)
        tree.build()
        tree_obj = tree.make_mobject()
        
        self.play(
            Create(tree.title),
            run_time=1
        )
        self.wait(1)
        
        self.play(
            Create(tree_obj),
            run_time=1
        )
        self.wait(1)

        order = [0, (0, 1), 1, (1, 2), 2, (2, 4), 4]
        wait_times = [0] * len(order)
        full_order = [tree.objects[i] if isinstance(i, int) else (tree.objects[i[0]], tree.objects[i[1]]) for i in order]
        tree.show_traversal(order, wait_times, run_time=0.3)
        self.wait(1)

