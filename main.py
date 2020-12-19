import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle
from speech import Speech


class MindMap:
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

		self.currentNodePerLevel = [0, 0, 0, 0]
		self.current_level = 0

		self.current_list = self.getCurrentList()
		self.current_node = 0

		self.G.add_edges_from(self.getCurrentEdges())
		self.node_colors = ['skyblue' if not node == self.currentNodeName() else 'yellow' for node in self.G.nodes()]

		self.update()


	def update(self):
		pos = dict([(self.current_list[i], [i, 0]) if i%2==0 else (self.current_list[i], [i, 1]) for i in range(len(self.current_list))])
		nx.draw_networkx_nodes(self.G, pos, cmap = plt.get_cmap('jet'), node_color = self.node_colors, node_size = 500)
		nx.draw_networkx_labels(self.G, pos)
		nx.draw_networkx_edges(self.G, pos, edgelist=self.getCurrentEdges(), arrows=False)
		print("updated MindMap")


	def getCurrentList(self):
		node = "root"

		for i in range(self.current_level + 1):
			level = self.levels[i][node]
			node = level[self.currentNodePerLevel[i]]

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


	def getIndex(self, l, i):
		while i >= len(l):
			i -= len(l)

		while i < 0:
			i += len(l)

		return i


	def currentNodeName(self):
		return self.current_list[self.current_node]


	def left(self):
		self.current_node = self.getIndex(self.current_list, self.current_node - 1)
		print("current_node", self.current_node)
		self.node_colors = ['skyblue' if not node == self.currentNodeName() else 'yellow' for node in self.G.nodes()]
	
		return

	def right(self):
		self.current_node = self.getIndex(self.current_list, self.current_node + 1)
		print("current_node", self.current_node)
		self.node_colors = ['skyblue' if not node == self.currentNodeName() else 'yellow' for node in self.G.nodes()]

		return


class MemorySpace(MindMap):
	def update(self):
		pos = dict([(self.current_list[i], [i, 0]) if i%2==0 else (self.current_list[i], [i, 1]) for i in range(len(self.current_list))])
		nx.draw_networkx_nodes(self.G, pos, cmap = plt.get_cmap('jet'), node_color = self.node_colors, node_size = 500)
		nx.draw_networkx_labels(self.G, pos)
		nx.draw_networkx_edges(self.G, pos, edgelist=self.getCurrentEdges(), edge_color='white', arrows=False)
		print("updated MemorySpace")


# left hand: sfed, r
# right hand: jlik, u
def keyboard_input(event):
	global mindmap
	global memoryspace

	# Left hand for memoryspace
	# new node
	if event.key == 'r':
		speech.read()
		# memoryspace.addSpeech(speech.read())
	if event.key == 's':
		memoryspace.left()
	elif event.key == 'f':
		memoryspace.right()
	elif event.key == 'e':
		memoryspace.up()
	elif event.key == 'd':
		memoryspace.down()

	# Right hand for mindmaps
	if event.key == 'j':
		mindmap.left()
	elif event.key == 'l':
		mindmap.right()
	elif event.key == 'i':
		mindmap.up()
	elif event.key == 'k':
		mindmap.down()

	plt.clf()

	memoryspace_plt = plt.subplot(1, 2, 1)
	memoryspace_plt.set_ylim(5, -5)
	memoryspace.update()
	
	mindmap_plt = plt.subplot(1, 2, 2)
	mindmap_plt.set_ylim(5, -5)
	mindmap.update()
	plt.draw()


speech = Speech()

# Disable keyboard shortcuts in Matplotlib
# print(plt.rcParams)
plt.rcParams['keymap.fullscreen'] = 'ctrl+f'
plt.rcParams['keymap.save'] = 'ctrl+s'

memoryspace_plt = plt.subplot(1, 2, 1)
memoryspace_plt.set_ylim(5, -5)
memoryspace = MemorySpace()

mindmap_plt = plt.subplot(1, 2, 2)
mindmap_plt.set_ylim(5, -5)
mindmap = MindMap()

plt.gcf().canvas.mpl_connect('key_press_event', keyboard_input)
plt.show()