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

		self.currentNodeValue_list = self.getCurrentNodeValueList()
		self.currentNode = 0

		self.G.add_edges_from(self.getCurrentEdges())
		self.node_colors = ['skyblue' if not node == self.currentNodeName() else 'yellow' for node in self.G.nodes()]

		self.update()


	def update(self):
		pos = dict([(self.currentNodeValue_list[i], [i, 0]) if i%2==0 else (self.currentNodeValue_list[i], [i, 1]) for i in range(len(self.currentNodeValue_list))])
		self.node_colors = ['skyblue' if not node == self.currentNodeName() else 'yellow' for node in self.G.nodes()]

		nx.draw_networkx_nodes(self.G, pos, cmap = plt.get_cmap('jet'), node_color = self.node_colors, node_size = 500)
		nx.draw_networkx_labels(self.G, pos)
		nx.draw_networkx_edges(self.G, pos, edgelist=self.getCurrentEdges(), arrows=False)
		print("updated MindMap")


	def getCurrentNodeValueList(self):
		nodeValue = "root"

		for i in range(self.current_level + 1):
			nodeValueListOfLevel_i = self.levels[i][nodeValue]
			nodeValue = nodeValueListOfLevel_i[self.currentNodePerLevel[i]]

		return nodeValueListOfLevel_i


	def getCurrentEdges(self):
		edges = []
		for i in range(len(self.currentNodeValue_list) - 1):
			edges.append((self.currentNodeValue_list[i], self.currentNodeValue_list[i+1]))

		return edges


	def getIndex(self, l, i):
		while i >= len(l):
			i -= len(l)

		while i < 0:
			i += len(l)

		return i


	def currentNodeName(self):
		return self.currentNodeValue_list[self.currentNode]


	def left(self):
		self.currentNode = self.getIndex(self.currentNodeValue_list, self.currentNode - 1)
	
		return


	def right(self):
		self.currentNode = self.getIndex(self.currentNodeValue_list, self.currentNode + 1)

		return


class MemorySpace(MindMap):
	def __init__(self):
		# super().__init__()
		self.G = nx.Graph()

		self.level0 = {"root": ["Hi", "Hello", "Hey", "What's up"]}
		self.levels = [self.level0]

		self.currentNodePerLevel = [0]
		self.current_level = 0

		self.currentNodeValue_list = self.getCurrentNodeValueList()
		self.currentNode = 0

		self.G.add_edges_from(self.getCurrentEdges())
		self.node_colors = ['skyblue' if not node == self.currentNodeName() else 'yellow' for node in self.G.nodes()]

		self.update()


	def update(self):
		pos = dict([(self.currentNodeValue_list[i], [i, 0]) if i%2==0 else (self.currentNodeValue_list[i], [i, 1]) for i in range(len(self.currentNodeValue_list))])
		self.node_colors = ['skyblue' if not node == self.currentNodeName() else 'yellow' for node in self.G.nodes()]

		nx.draw_networkx_nodes(self.G, pos, node_color = self.node_colors, node_size = 500)
		nx.draw_networkx_labels(self.G, pos)
		nx.draw_networkx_edges(self.G, pos, edgelist=self.getCurrentEdges(), edge_color='white', arrows=False)
		print("updated MemorySpace")


	def addSpeech(self, newSpeech):
		if len(self.getCurrentNodeValueList()) == 0:
			self.G.add_nodes_from([(newSpeech)])
			self.currentNode = 1

		else:
			lastNode = self.getCurrentNodeValueList()[-1]
			self.getCurrentNodeValueList().append(newSpeech)
			self.currentNode = len(self.getCurrentNodeValueList()) - 1
			self.G.add_edges_from([(lastNode, newSpeech)])

		return


# left hand: sfed, r
# right hand: jlik, u
def keyboard_input(event):
	global mindmap
	global memoryspace

	# Left hand for memoryspace
	# new node
	if event.key == 'r':
		newSpeech = speech.read()
		if newSpeech != "":
			memoryspace.addSpeech(newSpeech)
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