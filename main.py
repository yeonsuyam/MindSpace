import networkx as nx
import matplotlib.pyplot as plt

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle

class Mindmap:
	def __init__(self):
		self.G = nx.Graph()
		# self.Glevel1 = nx.Graph()
		# self.Glevel1.add_edges_from(
		# 	[("A", "B"), ("B", "C"), ("C", "D")])
		# self.Glevel2 = nx.Graph()
		# self.Glevel2.add_edges_from(
		# 	[("A", "B"), ("B", "C"), ("C", "D")])
		# self.Glevel3 = nx.Graph()
		# self.Glevel4 = nx.Graph()

		self.level0 = {"root": ["A", "B", "C", "D"]}
		self.level1 = {"A": ["a", "b", "c"], "B": ["d", "e"], "C": ["f"]}
		self.level2 = {}
		# self.level3 = {}
		self.levels = [self.level0, self.level1, self.level2]

		self.nodePerLevel = [1, 1, 0, 0]

		self.current_level = 1
		self.current_node = 1

		self.current_list = self.getCurrentList()

		self.G.add_edges_from(self.getCurrentEdges())

		red_nodes = []
		self.node_colors = ['skyblue' if not node in red_nodes else 'red' for node in self.G.nodes()]

		pos = nx.spring_layout(self.G)
		# nx.draw(self.G, cmap = plt.get_cmap('jet'), node_color = self.node_colors)
		nx.draw_networkx_nodes(self.G, pos, cmap = plt.get_cmap('jet'), node_color = self.node_colors, node_size = 500)
		nx.draw_networkx_labels(self.G, pos)
		nx.draw_networkx_edges(self.G, pos, edgelist=self.getCurrentEdges(), arrows=False)
		plt.show()


	def getCurrentList(self):
		node = "root"

		for i in range(self.current_level + 1):
			level = self.levels[i][node]
			node = level[self.nodePerLevel[i]]

		return level


	def getCurrentEdges(self):
		edges = []
		for i in range(len(self.current_list) - 1):
			edges.append((self.current_list[i], self.current_list[i+1]))

		# TODO
		# 만약에 아직 연결하지 않은 edge라면 흰색이나 투명색으로 edge 색상 설정
		# TODO
		# self.edge_colors = ['black' if not node in gray_nodes else 'gray' for node in self.G.nodes()]

		return edges


	def left(self):
		return
		# self.

# G = nx.Graph()
# G.add_edges_from(
#     [('A', 'A'), ('B', 'B')])

# G.add_node("hey how are you doing?")
# red_nodes = []
# node_colors = ['blue' if not node in red_nodes else 'red' for node in G.nodes()]


# Specify the edges you want here
# red_edges = [('A', 'C'), ('E', 'C')]
# edge_colours = ['black' if not edge in red_edges else 'red'
				# for edge in G.edges()]
# black_edges = [edge for edge in G.edges() if edge not in red_edges]

# pos = nx.spring_layout(G)
# nx.draw(G, cmap = plt.get_cmap('jet'), node_color = node_colors)
# nx.draw_networkx_labels(G, pos)




# left hand: sfed, r
# right hand: jlik, u
def keyboard_input(event):
	# new node
	if event.key == 'r':
		power += 1

	elif event.key == 'left':
		power -= 1

	plt.clf()
	plt.plot(data**power)
	plt.draw()


mindmap = Mindmap()