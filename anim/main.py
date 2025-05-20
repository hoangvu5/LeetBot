from manim import *
import random

class GraphNode:
	def __init__(self, data, position=ORIGIN, radius=0.5, neighbors=[], scale=1):
		self.char = data
		self.data = Text(str(data))
		self.data.scale(scale)
		self.neighbors = []
		self.center = position
		self.radius = radius
		self.circle = Circle(radius=radius)
		self.circle.move_to(position)
		self.data.move_to(position)
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

	def __repr__(self):
		return 'GraphNode({0})'.format(self.char)

	def __str__(self):
		return 'GraphNode({0})'.format(self.char)
	
class GraphAnimationUtils(Scene):
	def construct(self):
		self.show_dfs_intuition()

	def show_dfs_intuition(self):

		dfs_intuition_title = Text("DFS Intuition")
		dfs_intuition_title.scale(1.2)
		dfs_intuition_title.move_to(UP * 3.5)
		h_line = Line(LEFT, RIGHT).scale(FRAME_X_RADIUS - 1)
		h_line.next_to(dfs_intuition_title, DOWN)
		

		graph, edge_dict = self.create_dfs_graph()
		nodes, edges = self.make_graph_mobject(graph, edge_dict)
		entire_graph = VGroup(nodes, edges)

		self.play(
			Write(dfs_intuition_title),
			Create(h_line)
		)
		self.wait()

		self.play(
			Create(entire_graph),
			run_time=3
		)

		self.wait(18)

		dfs_full_order = dfs(graph, 0)
		wait_times = [0] * len(dfs_full_order)
		wait_time_dict = {}
		for i in range(len(graph)):
			wait_time_dict[i] = 0

		wait_time_dict[0] = 2
		wait_times[0] = 7
		wait_time_dict[1] = 3
		wait_times[1] = 6

		order = Text("Order: 0 1 2 3 5 6 7 8 9 4")
		order.shift(DOWN * 0.5)
		order.next_to(entire_graph, DOWN)
		self.play(
			Write(order[:6])
		)

		self.wait(5)
		
		all_highlights = []

		new_highlights = self.show_full_dfs_animation(graph, edge_dict, dfs_full_order[:5], order[6:], wait_times, wait_time_dict)
		all_highlights.extend(new_highlights)
		self.wait(10)
		graph[2].surround_circle.set_color(RED)
		self.wait(3)
		self.play(
			Indicate(graph[1].circle, color=BLUE),
			run_time=2
		)
		wait_time_dict[1] = 1
		self.indicate_neighbors(graph, 1, wait_time_dict)
		self.wait(2)

		wait_times[3] = 2 
		new_highlights = self.show_full_dfs_animation(graph, edge_dict, dfs_full_order[5:11], order[9:], wait_times, wait_time_dict)
		all_highlights.extend(new_highlights)
		self.wait()
		graph[6].surround_circle.set_color(RED)
		self.wait(3)
		self.play(
			Indicate(graph[5].circle, color=BLUE),
			run_time=2
		)
		self.indicate_neighbors(graph, 5, wait_time_dict)
		
		new_highlights = self.show_full_dfs_animation(graph, edge_dict, dfs_full_order[11:17], order[12:], wait_times, wait_time_dict)
		all_highlights.extend(new_highlights)
		graph[9].surround_circle.set_color(RED)
		self.play(
			Indicate(graph[8].circle, color=BLUE),
			run_time=2
		)

		self.wait(5)

		graph[8].surround_circle.set_color(RED)
		self.wait(4)
		self.play(
			Indicate(graph[7].circle, color=BLUE),
			run_time=2
		)
		self.wait(2)

		graph[7].surround_circle.set_color(RED)
		self.wait()
		self.play(
			Indicate(graph[5].circle, color=BLUE),
			run_time=2
		)
		self.wait(2)

		graph[5].surround_circle.set_color(RED)
		self.wait(2)
		self.play(
			Indicate(graph[3].circle, color=BLUE),
			run_time=2
		)
		self.wait(3)

		graph[3].surround_circle.set_color(RED)
		self.wait(3)
		self.play(
			Indicate(graph[1].circle, color=BLUE),
			run_time=2
		)

		self.indicate_neighbors(graph, 1, wait_time_dict)

		new_highlights = self.show_full_dfs_animation(graph, edge_dict, dfs_full_order[17:], order[-1:], wait_times, wait_time_dict)
		all_highlights.extend(new_highlights)

		graph[4].surround_circle.set_color(RED)
		self.wait()
		self.play(
			Indicate(graph[1].circle, color=BLUE),
			run_time=2
		)
		self.wait()

		graph[1].surround_circle.set_color(RED)
		self.wait()
		self.play(
			Indicate(graph[0].circle, color=BLUE),
			run_time=2
		)
		self.wait()

		graph[0].surround_circle.set_color(RED)
		self.wait(5)


		self.play(
			*[FadeOut(obj) for obj in all_highlights],
		)

		self.wait()

		wait_times = [0] * len(dfs_full_order)
		wait_time_dict = {}
		for i in range(len(graph)):
			wait_time_dict[i] = 0

		all_highlights = self.show_dfs_preorder(graph, edge_dict, dfs_full_order, wait_times)
		self.wait(5)
		self.play(
			*[FadeOut(h) for h in all_highlights],
			FadeOut(entire_graph)
		)

		graph, edge_dict = self.create_dfs_graph2()
		nodes, edges = self.make_graph_mobject(graph, edge_dict)
		entire_graph = VGroup(nodes, edges)

		self.play(
			FadeIn(entire_graph)
		)

		self.wait(2)

		order_1 = Text("Order 1: 0 1 2 3 5 6 7 8 9 4")
		order_1.move_to(order.get_center())
		self.play(
			ReplacementTransform(order, order_1)
		)
		self.wait()

		order_2 = Text("Order 2: 0 2 1 4 3 5 8 9 7 6")
		order_2.next_to(order, DOWN)
		self.play(
			Write(order_2[:7])
		)
		self.wait(14)

		dfs_second_full_order = dfs(graph, 0)

		wait_times[0] = 5
		wait_times[2] = 26
		wait_times[1] = 2
		wait_times[4] = 2
		wait_times[5] = 1
		wait_times[9] = 2
		wait_times[7] = 9
		new_highlights = self.show_second_dfs_preorder(graph, edge_dict, dfs_second_full_order, order_2[7:], wait_times)

		self.wait(7)
		
		self.play(
			*[FadeOut(obj) for obj in new_highlights],
			FadeOut(entire_graph),
			FadeOut(order_1),
			FadeOut(order_2),
			FadeOut(entire_graph),
			FadeOut(dfs_intuition_title),
			FadeOut(h_line)
		)

	def show_dfs_preorder(self, graph, edge_dict, full_order, 
		wait_times, scale_factor=1, run_time=1):
		i = 0
		angle = 180
		all_highlights = []
		for element in full_order:
			if isinstance(element, int):
				surround_circle = self.highlight_node(graph, element, 
					start_angle=angle/360 * TAU, scale_factor=scale_factor, run_time=run_time)
				all_highlights.append(surround_circle)
			else:
				last_edge = self.sharpie_edge(edge_dict, element[0], element[1], 
					scale_factor=scale_factor, run_time=run_time)
				angle = self.find_angle_of_intersection(graph, last_edge.get_end(), element[1])
				all_highlights.append(last_edge)
			self.wait(wait_times[i])
			i += 1
		return all_highlights

	def show_second_dfs_preorder(self, graph, edge_dict, full_order, order,
		wait_times, scale_factor=1, run_time=1):
		i = 0
		angle = 180
		new_highlights = []
		order_index = 0
		for element in full_order:
			if isinstance(element, int):
				surround_circle = self.highlight_node(graph, element, 
					start_angle=angle/360 * TAU, scale_factor=scale_factor, run_time=run_time)
				self.play(
					TransformFromCopy(graph[element].data, order[order_index])
				)
				order_index += 1
				new_highlights.append(surround_circle)
				graph[element].surround_circle = surround_circle
				self.wait(wait_times[element])
			else:
				last_edge = self.sharpie_edge(edge_dict, element[0], element[1], 
					scale_factor=scale_factor, run_time=run_time)
				angle = self.find_angle_of_intersection(graph, last_edge.get_end(), element[1])
				new_highlights.append(last_edge)
			
			i += 1

		return new_highlights

	def show_full_dfs_animation(self, graph, edge_dict, full_order, order,
		wait_times, wait_time_dict, scale_factor=1, run_time=1):
		i = 0
		angle = 180
		surround_circles = [0] * len(graph)
		order_index = 0
		new_highlights = []
		for element in full_order:
			if isinstance(element, int):
				surround_circle = self.highlight_node(graph, element, 
					start_angle=angle/360 * TAU, scale_factor=scale_factor, run_time=run_time)
				# print(type(graph[element].data), type(order[order_index]))
				self.play(
					TransformFromCopy(graph[element].data, order[order_index])
				)
				order_index += 1
				self.indicate_neighbors(graph, element, wait_time_dict)
				graph[element].surround_circle = surround_circle
				new_highlights.append(surround_circle)
				self.wait(wait_times[element])
			else:
				last_edge = self.sharpie_edge(edge_dict, element[0], element[1], 
					scale_factor=scale_factor, run_time=run_time)
				angle = self.find_angle_of_intersection(graph, last_edge.get_end(), element[1])
				new_highlights.append(last_edge)
			
			i += 1

		return new_highlights

	def indicate_neighbors(self, graph, i, wait_time_dict):
		current_node = graph[i]
		neighbors = current_node.neighbors
		self.wait(wait_time_dict[i])
		self.play(
			*[Indicate(neighbor.circle) for neighbor in neighbors],
			run_time=2
		)
		

	def create_dfs_graph(self):
		graph = []
		edges = {}

		radius, scale = 0.4, 0.9
		SHIFT = RIGHT * 2.5
		node_0 = GraphNode('0', position=LEFT * 5, radius=radius, scale=scale)
		node_1 = GraphNode('1', position=LEFT * 3 + UP * 2, radius=radius, scale=scale)
		node_2 = GraphNode('2', position=LEFT * 3 + DOWN * 2, radius=radius, scale=scale)
		node_3 = GraphNode('3', position=LEFT * 1, radius=radius, scale=scale)
		node_4 = GraphNode('4', position=LEFT * 1 + UP * 2, radius=radius, scale=scale)
		node_5 = GraphNode('5', position=RIGHT * 1, radius=radius, scale=scale)
		node_6 = GraphNode('6', position=LEFT * 1 + DOWN * 2, radius=radius, scale=scale)
		node_7 = GraphNode('7', position=RIGHT * 3 + DOWN * 2, radius=radius, scale=scale)
		node_8 = GraphNode('8', position=RIGHT * 3 + UP * 2, radius=radius, scale=scale)
		node_9 = GraphNode('9', position=RIGHT * 5 + UP * 2, radius=radius, scale=scale)

		edges[(0, 2)] = node_0.connect(node_2)
		edges[(0, 1)] = node_0.connect(node_1)

		edges[(1, 4)] = node_1.connect(node_4)
		edges[(1, 3)] = node_1.connect(node_3)
		edges[(1, 2)] = node_1.connect(node_2)

		edges[(3, 5)] = node_3.connect(node_5)

		edges[(5, 8)] = node_5.connect(node_8)
		edges[(5, 7)] = node_5.connect(node_7)
		edges[(5, 6)] = node_5.connect(node_6)

		edges[(7, 8)] = node_7.connect(node_8)

		edges[(8, 9)] = node_8.connect(node_9)

		graph.append(node_0)
		graph.append(node_1)
		graph.append(node_2)
		graph.append(node_3)
		graph.append(node_4)
		graph.append(node_5)
		graph.append(node_6)
		graph.append(node_7)
		graph.append(node_8)
		graph.append(node_9)

		return graph, edges

	def create_dfs_graph_directed(self):
		graph = []
		edges = {}

		radius, scale = 0.4, 0.9
		SHIFT = RIGHT * 2.5
		node_0 = GraphNode('0', position=LEFT * 5, radius=radius, scale=scale)
		node_1 = GraphNode('1', position=LEFT * 3 + UP * 2, radius=radius, scale=scale)
		node_2 = GraphNode('2', position=LEFT * 3 + DOWN * 2, radius=radius, scale=scale)
		node_3 = GraphNode('3', position=LEFT * 1, radius=radius, scale=scale)
		node_4 = GraphNode('4', position=LEFT * 1 + UP * 2, radius=radius, scale=scale)
		node_5 = GraphNode('5', position=RIGHT * 1, radius=radius, scale=scale)
		node_6 = GraphNode('6', position=LEFT * 1 + DOWN * 2, radius=radius, scale=scale)
		node_7 = GraphNode('7', position=RIGHT * 3 + DOWN * 2, radius=radius, scale=scale)
		node_8 = GraphNode('8', position=RIGHT * 3 + UP * 2, radius=radius, scale=scale)
		node_9 = GraphNode('9', position=RIGHT * 5 + UP * 2, radius=radius, scale=scale)

		edges[(0, 2)] = node_0.connect_arrow(node_2)
		edges[(0, 1)] = node_0.connect_arrow(node_1)

		edges[(1, 4)] = node_1.connect_arrow(node_4)
		edges[(1, 3)] = node_1.connect_arrow(node_3)
		edges[(1, 2)] = node_1.connect_arrow(node_2)

		edges[(3, 5)] = node_3.connect_arrow(node_5)

		edges[(5, 8)] = node_5.connect_arrow(node_8)
		edges[(5, 7)] = node_5.connect_arrow(node_7)
		edges[(5, 6)] = node_5.connect_arrow(node_6)

		edges[(7, 8)] = node_7.connect_arrow(node_8)

		edges[(8, 9)] = node_8.connect_arrow(node_9)

		graph.append(node_0)
		graph.append(node_1)
		graph.append(node_2)
		graph.append(node_3)
		graph.append(node_4)
		graph.append(node_5)
		graph.append(node_6)
		graph.append(node_7)
		graph.append(node_8)
		graph.append(node_9)

		return graph, edges

	def create_dfs_graph2(self):
		graph = []
		edges = {}

		radius, scale = 0.4, 0.9
		SHIFT = RIGHT * 2.5
		node_0 = GraphNode('0', position=LEFT * 5, radius=radius, scale=scale)
		node_1 = GraphNode('1', position=LEFT * 3 + UP * 2, radius=radius, scale=scale)
		node_2 = GraphNode('2', position=LEFT * 3 + DOWN * 2, radius=radius, scale=scale)
		node_3 = GraphNode('3', position=LEFT * 1, radius=radius, scale=scale)
		node_4 = GraphNode('4', position=LEFT * 1 + UP * 2, radius=radius, scale=scale)
		node_5 = GraphNode('5', position=RIGHT * 1, radius=radius, scale=scale)
		node_6 = GraphNode('6', position=LEFT * 1 + DOWN * 2, radius=radius, scale=scale)
		node_7 = GraphNode('7', position=RIGHT * 3 + DOWN * 2, radius=radius, scale=scale)
		node_8 = GraphNode('8', position=RIGHT * 3 + UP * 2, radius=radius, scale=scale)
		node_9 = GraphNode('9', position=RIGHT * 5 + UP * 2, radius=radius, scale=scale)

		
		edges[(0, 1)] = node_0.connect(node_1)
		edges[(0, 2)] = node_0.connect(node_2)

		edges[(1, 2)] = node_1.connect(node_2)
		edges[(1, 3)] = node_1.connect(node_3)
		edges[(1, 4)] = node_1.connect(node_4)

		edges[(3, 5)] = node_3.connect(node_5)

		edges[(5, 6)] = node_5.connect(node_6)
		edges[(5, 7)] = node_5.connect(node_7)
		edges[(5, 8)] = node_5.connect(node_8)

		edges[(7, 8)] = node_7.connect(node_8)

		edges[(8, 9)] = node_8.connect(node_9)

		graph.append(node_0)
		graph.append(node_1)
		graph.append(node_2)
		graph.append(node_3)
		graph.append(node_4)
		graph.append(node_5)
		graph.append(node_6)
		graph.append(node_7)
		graph.append(node_8)
		graph.append(node_9)

		return graph, edges

	def create_small_graph(self):
		graph = []
		edges = {}

		radius, scale = 0.4, 0.9
		node_0 = GraphNode('0', position=DOWN * 1 + LEFT * 3, radius=radius, scale=scale)
		node_1 = GraphNode('1', position=UP * 1 + LEFT, radius=radius, scale=scale)
		node_2 = GraphNode('2', position=DOWN * 3 + LEFT, radius=radius, scale=scale)
		node_3 = GraphNode('3', position=DOWN * 1 + RIGHT, radius=radius, scale=scale)
		node_4 = GraphNode('4', position=DOWN * 1 + RIGHT * 3, radius=radius, scale=scale)


		edges[(0, 3)] = node_0.connect(node_3)
		edges[(0, 2)] = node_0.connect(node_2)
		edges[(0, 1)] = node_0.connect(node_1)

		edges[(1, 3)] = node_1.connect(node_3)

		edges[(2, 3)] = node_2.connect(node_3)

		edges[(3, 4)] = node_3.connect(node_4)

		graph.append(node_0)
		graph.append(node_1)
		graph.append(node_2)
		graph.append(node_3)
		graph.append(node_4)

		return graph, edges

	def create_small_directed_graph(self):
		graph = []
		edges = {}

		radius, scale = 0.4, 0.9
		node_0 = GraphNode('0', position=DOWN * 1 + LEFT * 3, radius=radius, scale=scale)
		node_1 = GraphNode('1', position=UP * 1 + LEFT, radius=radius, scale=scale)
		node_2 = GraphNode('2', position=DOWN * 3 + LEFT, radius=radius, scale=scale)
		node_3 = GraphNode('3', position=DOWN * 1 + RIGHT, radius=radius, scale=scale)
		node_4 = GraphNode('4', position=DOWN * 1 + RIGHT * 3, radius=radius, scale=scale)


		edges[(0, 1)] = node_0.connect_arrow(node_1)
		edges[(0, 2)] = node_2.connect_arrow(node_0)
		edges[(0, 3)] = node_0.connect_arrow(node_3)

		edges[(1, 3)] = node_1.connect_arrow(node_3)

		edges[(2, 3)] = node_3.connect_arrow(node_2)

		edges[(3, 4)] = node_3.connect_arrow(node_4)

		graph.append(node_0)
		graph.append(node_1)
		graph.append(node_2)
		graph.append(node_3)
		graph.append(node_4)

		return graph, edges

	def show_path(self, graph, edge_dict, path, scale_factor=1):
		angle = 180
		objects = []
		for i in range(len(path) - 1):
			u, v = path[i], path[i + 1]
			surround_circle = self.highlight_node(graph, u, start_angle=angle/360 * TAU, scale_factor=scale_factor)
			last_edge = self.sharpie_edge(edge_dict, u, v, scale_factor=scale_factor)
			objects.extend([surround_circle, last_edge])
			angle = self.find_angle_of_intersection(graph, last_edge.get_end(), v)

		if v != path[0]:
			surround_circle = self.highlight_node(graph, v, start_angle=angle/360 * TAU, scale_factor=scale_factor)
			objects.append(surround_circle)

		return objects

	def show_path_in_graph(self, graph, edge_dict, scale_factor=1):
		self.highlight_node(graph, 0, scale_factor=scale_factor)
		
		last_edge = self.sharpie_edge(edge_dict, 0, 6, scale_factor=scale_factor)
		angle = self.find_angle_of_intersection(graph, last_edge.get_end(), 6)
		self.highlight_node(graph, 6, start_angle=angle/360 * TAU, scale_factor=scale_factor)
		
		last_edge = self.sharpie_edge(edge_dict, 6, 7, scale_factor=scale_factor)
		angle = self.find_angle_of_intersection(graph, last_edge.get_end(), 7)
		self.highlight_node(graph, 7, start_angle=angle/360 * TAU, scale_factor=scale_factor)
		
		last_edge = self.sharpie_edge(edge_dict, 7, 3, scale_factor=scale_factor)
		angle = self.find_angle_of_intersection(graph, last_edge.get_end(), 3)
		self.highlight_node(graph, 3, start_angle=angle/360 * TAU, scale_factor=scale_factor)
		
		last_edge = self.sharpie_edge(edge_dict, 3, 2, scale_factor=scale_factor)
		angle = self.find_angle_of_intersection(graph, last_edge.get_end(), 2)
		self.highlight_node(graph, 2, start_angle=angle/360 * TAU, scale_factor=scale_factor)

	def find_angle_of_intersection(self, graph, last_point, node_index):
		node = graph[node_index]
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

	def highlight_edge(self, edge_dict, v, u, color=GREEN):
		switch = False
		if v > u:
			u, v = v, u
			switch = True
		edge = edge_dict[(v, u)]
		normal_1, normal_2 = edge.get_unit_normals()
		scale_factor = 1.5
		if not switch:
			line_1 = Line(edge.get_start() + normal_1 * SMALL_BUFF / scale_factor,
				edge.get_end() + normal_1 * SMALL_BUFF / scale_factor)
			line_2 = Line(edge.get_start() + normal_2 * SMALL_BUFF / scale_factor,
				edge.get_end() + normal_2 * SMALL_BUFF / scale_factor)
		else:
			line_1 = Line(edge.get_end() + normal_1 * SMALL_BUFF / scale_factor,
				edge.get_start() + normal_1 * SMALL_BUFF / scale_factor)
			line_2 = Line(edge.get_end() + normal_2 * SMALL_BUFF / scale_factor,
				edge.get_start() + normal_2 * SMALL_BUFF / scale_factor)
					
		line_1.set_stroke(width=8)
		line_2.set_stroke(width=8)
		line_1.set_color(color)
		line_2.set_color(color)

		self.play(
			Create(line_1),
			Create(line_2),
		)

	def sharpie_edge(self, edge_dict, u, v, color=GREEN, 
		scale_factor=1, animate=True, run_time=1):
		switch = False
		if u > v:
			edge = edge_dict[(v, u)]
			switch = True
		else:
			edge = edge_dict[(u, v)]
		
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

	def highlight_node(self, graph, index, color=GREEN, 
		start_angle=TAU/2, scale_factor=1, animate=True, run_time=1):
		node = graph[index]
		surround_circle = Circle(radius=node.circle.radius * scale_factor)
		surround_circle.move_to(node.circle.get_center())
		# surround_circle.scale(1.15)
		surround_circle.set_stroke(width=8 * scale_factor)
		surround_circle.set_color(color)
		surround_circle.set_fill(opacity=0)
		if animate:
			self.play(
				Create(surround_circle),
				run_time=run_time
			)
		return surround_circle

	def create_initial_graph(self):
		graph = []
		edges = {}

		radius, scale = 0.4, 0.9
		SHIFT = RIGHT * 2.5
		node_0 = GraphNode('0', position=LEFT * 2.5, radius=radius, scale=scale)
		node_1 = GraphNode('1', position=RIGHT * 3, radius=radius, scale=scale)
		node_2 = GraphNode('2', position=RIGHT * 1.5 + UP, radius=radius, scale=scale)
		node_3 = GraphNode('3', position=UP * 2.5 + SHIFT, radius=radius, scale=scale)
		node_4 = GraphNode('4', position=DOWN * 2, radius=radius, scale=scale)
		node_5 = GraphNode('5', position=DOWN + RIGHT * 2, radius=radius, scale=scale)
		node_6 = GraphNode('6', position=LEFT + UP, radius=radius, scale=scale)
		node_7 = GraphNode('7', position=LEFT  * 2 + UP * 2 + SHIFT, radius=radius, scale=scale)
		node_8 = GraphNode('8', position=ORIGIN, radius=radius, scale=scale)

		edge_0_6 = node_0.connect(node_6)
		edges[(0, 6)] = edge_0_6
		# edges[(6, 0)] = edge_0_6
		edge_0_8 = node_0.connect(node_8)
		edges[(0, 8)] = edge_0_8
		# edges[(8, 0)] = edge_0_8
		edge_0_4 = node_0.connect(node_4)
		edges[(0, 4)] = edge_0_4
		# edges[(4, 0)] = edge_0_4
		edge_1_2 = node_1.connect(node_2)
		edges[(1, 2)] = edge_1_2
		# edges[(2, 1)] = edge_1_2
		edge_1_5 = node_1.connect(node_5)
		edges[(1, 5)] = edge_1_5
		# edges[(5, 1)] = edge_1_5
		edge_2_3 = node_2.connect(node_3)
		edges[(2, 3)] = edge_2_3
		# edges[(3, 2)] = edge_2_3
		edge_3_7 = node_3.connect(node_7)
		edges[(3, 7)] = edge_3_7
		# edges[(7, 3)] = edge_3_7
		edge_4_5 =  node_4.connect(node_5)
		edges[(4, 5)] = edge_4_5
		# edges[(5, 4)] = edge_4_5
		edge_6_7 = node_6.connect(node_7)
		edges[(6, 7)] = edge_6_7
		# edges[(7, 6)] = edge_6_7
		edge_1_8 = node_1.connect(node_8)
		edges[(1, 8)] = edge_1_8
		# edges[(8, 1)] = edge_1_8

		graph.append(node_0)
		graph.append(node_1)
		graph.append(node_2)
		graph.append(node_3)
		graph.append(node_4)
		graph.append(node_5)
		graph.append(node_6)
		graph.append(node_7)
		graph.append(node_8)

		return graph, edges	

	def create_disconnected_graph(self):
		graph = []
		edges = {}

		radius, scale = 0.4, 0.9
		SHIFT = RIGHT * 2.5
		right_shift = RIGHT * 0.5
		left_shift = LEFT * 0.5
		node_0 = GraphNode('0', position=LEFT * 2.5 + left_shift, radius=radius, scale=scale)
		node_1 = GraphNode('1', position=RIGHT * 3 + right_shift, radius=radius, scale=scale)
		node_2 = GraphNode('2', position=RIGHT * 1.5 + UP + right_shift, radius=radius, scale=scale)
		node_3 = GraphNode('3', position=UP * 2.5 + SHIFT + right_shift, radius=radius, scale=scale)
		node_4 = GraphNode('4', position=DOWN * 2 + left_shift, radius=radius, scale=scale)
		node_5 = GraphNode('5', position=DOWN + RIGHT * 2 + right_shift, radius=radius, scale=scale)
		node_6 = GraphNode('6', position=LEFT + UP + left_shift, radius=radius, scale=scale)
		node_7 = GraphNode('7', position=LEFT  * 2 + UP * 2 + SHIFT + left_shift, radius=radius, scale=scale)
		node_8 = GraphNode('8', position=ORIGIN + left_shift, radius=radius, scale=scale)

		edge_0_6 = node_0.connect(node_6)
		edges[(0, 6)] = edge_0_6

		edge_0_8 = node_0.connect(node_8)
		edges[(0, 8)] = edge_0_8

		edge_0_4 = node_0.connect(node_4)
		edges[(0, 4)] = edge_0_4

		edge_1_2 = node_1.connect(node_2)
		edges[(1, 2)] = edge_1_2

		edge_1_5 = node_1.connect(node_5)
		edges[(1, 5)] = edge_1_5

		edge_2_3 = node_2.connect(node_3)
		edges[(2, 3)] = edge_2_3

		edge_6_7 = node_6.connect(node_7)
		edges[(6, 7)] = edge_6_7



		graph.append(node_0)
		graph.append(node_1)
		graph.append(node_2)
		graph.append(node_3)
		graph.append(node_4)
		graph.append(node_5)
		graph.append(node_6)
		graph.append(node_7)
		graph.append(node_8)

		return graph, edges

	def make_graph_mobject(self, graph, edge_dict, node_color=DARK_BLUE, 
		stroke_color=BLUE, data_color=WHITE, edge_color=GRAY, scale_factor=1,
		show_data=True):
		nodes = []
		edges = []
		for node in graph:
			node.circle.set_fill(color=node_color, opacity=0.5)
			node.circle.set_stroke(color=stroke_color)
			node.data.set_color(color=data_color)
			if show_data:
				nodes.append(VGroup(node.circle, node.data))
			else:
				nodes.append(node.circle)
		for edge in edge_dict.values():
			edge.set_stroke(width=7*scale_factor)
			edge.set_color(color=edge_color)
			edges.append(edge)
		return VGroup(*nodes), VGroup(*edges)
	

class Introduction(GraphAnimationUtils):
	def construct(self):
		graph, edge_dict = self.create_huge_graph()
		nodes, edges = self.make_graph_mobject(graph, edge_dict, show_data=False)
		entire_graph = VGroup(nodes, edges)

		self.play(
			Create(entire_graph),
			run_time=1
		)
		self.wait()

		dfs_full_order = dfs_maze(graph, 4)
		wait_times = [0] * len(dfs_full_order)

		self.show_dfs_preorder(graph, edge_dict, dfs_full_order, wait_times, 
			scale_factor=1, run_time=0.3)

		self.wait()

	def create_huge_graph(self):
		x_coords = list(range(-5, 6))
		y_coords_1 = list(np.arange(-3, 4, 1))
		y_coords_2 = list(np.arange(-2.5, 3, 1))
		graph = []
		edges = {}
		radius = 0.2
		scale = 0.5

		node_id = 0
		for i in range(len(x_coords)):
			if i % 2 == 0:
				y_coords = y_coords_1
			else:
				y_coords = y_coords_2
			for j in range(len(y_coords)):
				node = GraphNode(str(node_id), position=RIGHT * x_coords[i] + DOWN * y_coords[j], 
					radius=radius, scale=scale)
				graph.append(node)
				node_id += 1

		for i in range(node_id):
			if i < 65 and i % 13 != 6:
				edges[(i, i + 7)] = graph[i].connect(graph[i + 7])
			if i < 65 and i % 13 != 0:
				edges[(i, i + 6)] = graph[i].connect(graph[i + 6])

		return graph, edges
	
def dfs_maze(graph, start):
	"""
	Returns a list of vertices and edges in preorder traversal
	"""
	dfs_order = []
	marked = [False] * len(graph)
	edge_to = [None] * len(graph)

	stack = [start]
	while len(stack) > 0:
		node = stack.pop()
		if not marked[node]:
			marked[node] = True
			dfs_order.append(node)
		neighbor_nodes = []
		for neighbor in graph[node].neighbors:
			neighbor_node = int(neighbor.char)
			if not marked[neighbor_node]:
				edge_to[neighbor_node] = node
				neighbor_nodes.append(neighbor_node)
		random.shuffle(neighbor_nodes)
		stack.extend(neighbor_nodes)

	print(dfs_order)
	dfs_full_order = []
	for i in range(len(dfs_order) - 1):
		prev, curr = dfs_order[i], dfs_order[i + 1]
		dfs_full_order.append(prev)
		dfs_full_order.append((edge_to[curr], curr))

	dfs_full_order.append(curr)
	print(dfs_full_order)
	return dfs_full_order

def dfs(graph, start):
	"""
	Returns a list of vertices and edges in preorder traversal
	"""
	dfs_order = []
	marked = [False] * len(graph)
	edge_to = [None] * len(graph)

	stack = [start]
	while len(stack) > 0:
		node = stack.pop()
		if not marked[node]:
			marked[node] = True
			dfs_order.append(node)
		for neighbor in graph[node].neighbors:
			neighbor_node = int(neighbor.char)
			if not marked[neighbor_node]:
				edge_to[neighbor_node] = node
				stack.append(neighbor_node)

	print(dfs_order)
	dfs_full_order = []
	for i in range(len(dfs_order) - 1):
		prev, curr = dfs_order[i], dfs_order[i + 1]
		dfs_full_order.append(prev)
		dfs_full_order.append((edge_to[curr], curr))

	dfs_full_order.append(curr)
	print(dfs_full_order)
	return dfs_full_order