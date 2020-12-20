import networkx as nx
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from itertools import cycle
from speech import Speech


class MindMap:
	def __init__(self):
		self.currentG = nx.Graph()
		self.topG = nx.Graph()
		self.bottomG = nx.Graph()
		# self.Glevel1 = nx.Graph()
		# self.Glevel1.add_edges_from(
		# 	[("A", "B"), ("B", "C"), ("C", "D")])
		# self.Glevel2 = nx.Graph()
		# self.Glevel2.add_edges_from(
		# 	[("A", "B"), ("B", "C"), ("C", "D")])
		# self.Glevel3 = nx.Graph()
		# self.Glevel4 = nx.Graph()

		self.level0 = {"root": []}
		self.level1 = {}
		self.level2 = {}
		self.level3 = {}
		self.levels = [self.level0, self.level1, self.level2]

		self.currentNodePerLevel = [-1, -1, -1, -1]
		self.current_level = 0

		self.currentNodeValue_list = self.getCurrentNodeValueList()
		self.currentNode = -1

		self.currentG.add_edges_from(self.getCurrentEdges())
		self.node_colors = ['skyblue' if not node == self.currentNodeValue() else 'yellow' for node in self.currentG.nodes()]

		self.updateCurrent()


	def updateCurrent(self):
		pos = dict([(self.currentNodeValue_list[i], [i, 0]) if i%2==0 else (self.currentNodeValue_list[i], [i, 1]) for i in range(len(self.currentNodeValue_list))])
		self.node_colors = ['skyblue' if not node == self.currentNodeValue() else 'yellow' for node in self.currentG.nodes()]

		nx.draw_networkx_nodes(self.currentG, pos, cmap = plt.get_cmap('jet'), node_color = self.node_colors, node_size = 500)
		nx.draw_networkx_labels(self.currentG, pos, font_family = 'AppleGothic')
		nx.draw_networkx_edges(self.currentG, pos, edgelist=self.getCurrentEdges(), arrows=False)
		print("updateCurrent MindMap")
		print("MindMap", self.currentNodeValue_list, self.currentNode)


	def updateTop(self):
		# TODO: Show header of upper node if it is note "root"
		pos = dict([(node, [0, -5]) for node in self.topG.nodes()])
		self.node_colors = ['gray' for node in self.topG.nodes()]

		nx.draw_networkx_nodes(self.topG, pos, cmap = plt.get_cmap('jet'), node_color = self.node_colors, node_size = 500)
		nx.draw_networkx_labels(self.topG, pos, font_family = 'AppleGothic')
		print("updateTop MindMap")
		print("MindMap", self.currentNodeValue_list, self.currentNode)


	def getCurrentNodeValueList(self):
		nodeValue = "root"

		for i in range(self.current_level + 1):
			nodeValueListOfLevel_i = self.levels[i][nodeValue]
			if self.currentNodePerLevel[i] != -1:
				nodeValue = nodeValueListOfLevel_i[self.currentNodePerLevel[i]]

		return nodeValueListOfLevel_i


	def getLevelNodeValueList(self, level):
		nodeValue = "root"

		for i in range(self.level + 1):
			nodeValueListOfLevel_i = self.levels[i][nodeValue]
			if self.currentNodePerLevel[i] != -1:
				nodeValue = nodeValueListOfLevel_i[self.currentNodePerLevel[i]]

		return nodeValueListOfLevel_i


	def getCurrentEdges(self):
		edges = []
		for i in range(len(self.currentNodeValue_list) - 1):
			edges.append((self.currentNodeValue_list[i], self.currentNodeValue_list[i+1]))

		return edges


	def getIndex(self, l, i):
		if len(l) == 0: 
			return -1

		while i >= len(l):
			i -= len(l)

		while i < 0:
			i += len(l)

		return i


	def currentNodeValue(self):
		if self.currentNode != -1:
			return self.currentNodeValue_list[self.currentNode]
		else:
			return -1


	def addNode(self, newSpeech):
		self.levels[self.current_level + 1][newSpeech] = []

		if len(self.getCurrentNodeValueList()) == 0:
			self.getCurrentNodeValueList().append(newSpeech)
			self.currentG.add_nodes_from([(newSpeech)])
			self.currentNode = 0

		elif self.currentNode == len(self.getCurrentNodeValueList()) - 1:
			self.getCurrentNodeValueList().append(newSpeech)
			self.currentNode += 1
			leftNodeValue = self.getCurrentNodeValueList()[self.currentNode - 1]
			self.currentG.add_edges_from([(leftNodeValue, newSpeech)])

		else:
			self.getCurrentNodeValueList().insert(self.currentNode + 1, newSpeech)
			self.currentNode += 1
			leftNodeValue = self.getCurrentNodeValueList()[self.currentNode - 1]
			rightNodeValue = self.getCurrentNodeValueList()[self.currentNode + 1]
			self.currentG.remove_edge(leftNodeValue, rightNodeValue)
			self.currentG.add_edges_from([(leftNodeValue, newSpeech), (newSpeech, rightNodeValue)])
			
		return


	def left(self):
		if self.currentNode == -1:
			return

		self.currentNode = self.getIndex(self.currentNodeValue_list, self.currentNode - 1)
	
		return


	def right(self):
		if self.currentNode == -1:
			return
		
		self.currentNode = self.getIndex(self.currentNodeValue_list, self.currentNode + 1)

		return


	def bottomLevel(self):
		if self.currentNode == -1:
			return

		if self.current_level == 3:
			print("NOT IMPLEMENTED")
			return

		self.topG.add_node(self.currentNodeValue())

		self.currentNodePerLevel[self.current_level] = self.currentNode
		
		self.current_level += 1
		self.currentNodeValue_list = self.getCurrentNodeValueList()
		self.currentNode = 0 if len(self.currentNodeValue_list) != 0 else -1

		self.currentG.clear()
		if len(self.currentNodeValue_list) == 1:
			self.currentG.add_nodes_from(self.currentNodeValue_list)
		else:
			self.currentG.add_edges_from(self.getCurrentEdges())

		return


	def topLevel(self):
		if self.current_level == 0:
			print("topLevel: Error")
			return

		elif self.current_level == 1:
			self.topG.clear()

		else:
			parentNodeValueList = self.getLevelNodeValueList(self.current_level-1)
			parentNodeValue = parentNodeValueList[self.currentNodePerLevel[self.current_level-1]]
			self.topG.clear()
			self.topG.add_node(parentNodeValue)

		self.currentNodePerLevel[self.current_level] = self.currentNode

		self.current_level -= 1
		self.currentNodeValue_list = self.getCurrentNodeValueList()
		self.currentNode = self.currentNodePerLevel[self.current_level]

		self.currentG.clear()
		if len(self.currentNodeValue_list) == 1:
			self.currentG.add_nodes_from(self.currentNodeValue_list)
		else:
			self.currentG.add_edges_from(self.getCurrentEdges())

		return


class MemorySpace(MindMap):
	def __init__(self):
		# super().__init__()
		self.currentG = nx.Graph()

		self.level0 = {"root": []}
		self.levels = [self.level0]

		self.currentNodePerLevel = [-1]
		self.current_level = 0

		self.currentNodeValue_list = self.getCurrentNodeValueList()
		self.currentNode = -1

		self.currentG.add_edges_from(self.getCurrentEdges())
		self.node_colors = ['skyblue' if not node == self.currentNodeValue() else 'yellow' for node in self.currentG.nodes()]

		self.updateCurrent()


	def updateCurrent(self):
		pos = dict([(self.currentNodeValue_list[i], [i, 0]) if i%2==0 else (self.currentNodeValue_list[i], [i, 1]) for i in range(len(self.currentNodeValue_list))])
		self.node_colors = ['skyblue' if not node == self.currentNodeValue() else 'yellow' for node in self.currentG.nodes()]

		nx.draw_networkx_nodes(self.currentG, pos, node_color = self.node_colors, node_size = 500)
		nx.draw_networkx_labels(self.currentG, pos, font_family = 'AppleGothic')
		nx.draw_networkx_edges(self.currentG, pos, edgelist=self.getCurrentEdges(), edge_color='white', arrows=False)
		print("updateCurrentd MemorySpace")
		print("MemorySpace", self.currentNodeValue_list, self.currentNode)


	def addSpeech(self, newSpeech):
		if len(self.getCurrentNodeValueList()) == 0:
			self.currentG.add_nodes_from([(newSpeech)])
			self.getCurrentNodeValueList().append(newSpeech)
			self.currentNode = 0

		else:
			lastNodeValue = self.getCurrentNodeValueList()[-1]
			self.getCurrentNodeValueList().append(newSpeech)
			self.currentNode = len(self.getCurrentNodeValueList()) - 1
			self.currentG.add_edges_from([(lastNodeValue, newSpeech)])

		return


	def popCurrentNode(self):
		currentNodeValueList = self.getCurrentNodeValueList()
		currentNodeValue = currentNodeValueList[self.currentNode]
		try:
			leftNodeValue = currentNodeValueList[self.currentNode-1]
			leftNode = self.currentNode-1
		except:
			leftNode = -1
		try:
			rightNodeValue = currentNodeValueList[self.currentNode+1]
			rightNode = self.currentNode+1
		except:
			rightNode = -1
		
		self.getCurrentNodeValueList().pop(self.currentNode)
		self.currentG.remove_node(currentNodeValue)

		if leftNode	!= -1 and rightNode != -1:
			self.currentG.add_edge(leftNodeValue, rightNodeValue)

		self.currentNode = leftNode if leftNode != -1 else (rightNode-1)

		return currentNodeValue


# left hand: sfed, r
# right hand: jlik, u
def keyboard_input(event):
	global mindmap
	global memoryspace

	updateTop = False

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
	elif event.key == 'd':
		memoryspace.down()

		mindmap.addNode(memoryspace.popCurrentNode())
	# Right hand for mindmaps
	if event.key == 'j':
		mindmap.left()
	elif event.key == 'l':
		mindmap.right()
	elif event.key == 'i':
		mindmap.bottomLevel()
		updateTop = True
	elif event.key == 'k':
		mindmap.topLevel()
		updateTop = True

	plt.clf()

	memoryspace_plt = plt.subplot(1, 2, 1)
	memoryspace_plt.set_ylim(5, -5)
	memoryspace.updateCurrent()

	mindmap_plt = plt.subplot(1, 2, 2)
	mindmap_plt.set_ylim(5, -5)
	mindmap.updateCurrent()
	if updateTop:
		mindmap.updateTop()		

	plt.draw()


speech = Speech()

# Disable keyboard shortcuts in Matplotlib
# print(plt.rcParams)
plt.rcParams['keymap.fullscreen'] = 'ctrl+f'
plt.rcParams['keymap.save'] = 'ctrl+s'
mpl.rcParams['axes.unicode_minus'] = False

memoryspace_plt = plt.subplot(1, 2, 1)
memoryspace_plt.set_ylim(5, -5)
memoryspace = MemorySpace()

mindmap_plt = plt.subplot(1, 2, 2)
mindmap_plt.set_ylim(5, -5)
mindmap = MindMap()

plt.gcf().canvas.mpl_connect('key_press_event', keyboard_input)
plt.show()