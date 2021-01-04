import networkx as nx
import matplotlib.pyplot as plt


class MindMap:
	def __init__(self, axes):
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

		self.axes = axes

		self.level0 = {"root": []}
		self.level1 = {}
		self.level2 = {}
		self.level3 = {}
		self.level4 = {}
		self.levels = [self.level0, self.level1, self.level2, self.level3, self.level4]

		self.currentNodePerLevel = [-1, -1, -1, -1]
		self.current_level = 0

		self.currentNodeValue_list = self.getCurrentLevelNodeValueList()
		self.currentNode = -1

		self.currentG.add_edges_from(self.getCurrentEdges())
		self.node_colors = ['skyblue' if not node == self.currentNodeValue() else 'yellow' for node in self.currentG.nodes()]

		self.updateCurrent()


	def updateCurrent(self):
		pos = self.getPos(self.currentNodeValue_list)
		self.node_colors = ['skyblue' if not node == self.currentNodeValue() else 'yellow' for node in self.currentG.nodes()]

		nx.draw_networkx_nodes(self.currentG, pos, ax = self.axes, cmap = plt.get_cmap('jet'), node_color = self.node_colors, node_size = 2000)
		nx.draw_networkx_labels(self.currentG, pos, ax = self.axes, font_family = 'AppleGothic')
		nx.draw_networkx_edges(self.currentG, pos, ax = self.axes, edgelist=self.getCurrentEdges(), arrows=False)
		self.axes.axis('off')
		print("MindMap", "currentLevel: ", self.current_level, self.currentNodeValue_list, "currentNode: ", self.currentNode)
		print(self.level0, self.level1, self.level2, self.level3, self.level4)

		return


	def updateTop(self):
		# TODO: Show header of upper node if it is note "root"
		pos = dict([(node, [0, 5]) for node in self.topG.nodes()])
		self.node_colors = ['gray' for node in self.topG.nodes()]

		nx.draw_networkx_nodes(self.topG, pos, cmap = plt.get_cmap('jet'), node_color = self.node_colors, node_size = 2000)
		nx.draw_networkx_labels(self.topG, pos, font_family = 'AppleGothic')
		self.axes.axis('off')

		return


	def redrawCurrent(self):
		self.currentNodeValue_list = self.getCurrentLevelNodeValueList()
		self.currentG.clear()
		if len(self.currentNodeValue_list) == 1:
			self.currentG.add_nodes_from(self.currentNodeValue_list)
		else:
			self.currentG.add_edges_from(self.getCurrentEdges())

		return


	def getPos(self, l):
		return dict([(l[i], [i - (len(l)-1)/2.0, 2]) if i%2==0 else (l[i], [i - (len(l)-1)/2.0, -2]) for i in range(len(l))])


	def getCurrentLevelNodeValueList(self):
		nodeValue = "root"

		for i in range(self.current_level + 1):
			nodeValueListOfLevel_i = self.levels[i][nodeValue]
			if self.currentNodePerLevel[i] != -1:
				nodeValue = nodeValueListOfLevel_i[self.currentNodePerLevel[i]]

		return nodeValueListOfLevel_i


	def getLevelNodeValueList(self, level):
		nodeValue = "root"

		for i in range(level + 1):
			nodeValueListOfLevel_i = self.levels[i][nodeValue]
			if self.currentNodePerLevel[i] != -1:
				nodeValue = nodeValueListOfLevel_i[self.currentNodePerLevel[i]]

		return nodeValueListOfLevel_i


	def getKeyOfTopLevel(self):
		if self.current_level == 0:
			keyOfTopLevel = "root"
		else:
			keyOfTopLevel = self.getLevelNodeValueList(self.current_level-1)[self.currentNodePerLevel[self.current_level-1]]
		
		return keyOfTopLevel


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
		if newSpeech == None:
			print("Error: No node to add")
			return
		
		self.levels[self.current_level + 1][newSpeech] = []

		if len(self.getCurrentLevelNodeValueList()) == 0:
			self.getCurrentLevelNodeValueList().append(newSpeech)
			self.currentG.add_nodes_from([(newSpeech)])
			self.currentNode = 0

		elif self.currentNode == len(self.getCurrentLevelNodeValueList()) - 1:
			self.getCurrentLevelNodeValueList().append(newSpeech)
			self.currentNode += 1
			leftNodeValue = self.getCurrentLevelNodeValueList()[self.currentNode - 1]
			self.currentG.add_edges_from([(leftNodeValue, newSpeech)])

		else:
			self.getCurrentLevelNodeValueList().insert(self.currentNode + 1, newSpeech)
			self.currentNode += 1
			leftNodeValue = self.getCurrentLevelNodeValueList()[self.currentNode - 1]
			rightNodeValue = self.getCurrentLevelNodeValueList()[self.currentNode + 1]
			self.currentG.remove_edge(leftNodeValue, rightNodeValue)
			self.currentG.add_edges_from([(leftNodeValue, newSpeech), (newSpeech, rightNodeValue)])
			
		return


	def addNodeToBottomLevel(self, newSpeech):
		if newSpeech == None:
			print("Error: No node to add")
			return

		self.toBottomLevel()
		self.currentNode = len(self.currentNodeValue_list) - 1
		self.addNode(newSpeech)

		return


	def moveNodeToLeft(self):
		keyOfTopLevel = self.getKeyOfTopLevel()
		dictOfCurrentLevel = self.levels[self.current_level]

		l = self.getCurrentLevelNodeValueList()
		x = self.currentNode

		if x == 0:
			dictOfCurrentLevel[keyOfTopLevel] = l[x+1:] + [l[x]]
		else:
			dictOfCurrentLevel[keyOfTopLevel] = l[:x-1] + [l[x]] + l[x-1:x] + l[x+1:]

		self.currentNode = self.getIndex(self.currentNodeValue_list, self.currentNode - 1)
		self.redrawCurrent()

		return


	def moveNodeToRight(self):
		keyOfTopLevel = self.getKeyOfTopLevel()
		dictOfCurrentLevel = self.levels[self.current_level]

		l = self.getCurrentLevelNodeValueList()
		x = self.currentNode

		if x == len(l) - 1:
			dictOfCurrentLevel[keyOfTopLevel] = [l[x]] + l[:x]	
		else:
			dictOfCurrentLevel[keyOfTopLevel] = l[:x] + l[x+1:x+2] + [l[x]] + l[x+2:]

		self.currentNode = self.getIndex(self.currentNodeValue_list, self.currentNode + 1)
		self.redrawCurrent()

		return


	def toLeftNode(self):
		if self.currentNode == -1:
			return

		self.currentNode = self.getIndex(self.currentNodeValue_list, self.currentNode - 1)
	
		for i in range(len(self.currentNodePerLevel)):
			if i > self.current_level:
				self.currentNodePerLevel[i] = -1

		return


	def toRightNode(self):
		if self.currentNode == -1:
			return
		
		self.currentNode = self.getIndex(self.currentNodeValue_list, self.currentNode + 1)

		for i in range(len(self.currentNodePerLevel)):
			if i > self.current_level:
				self.currentNodePerLevel[i] = -1	

		return


	def toBottomLevel(self):
		if self.currentNode == -1:
			return

		if self.current_level == 3:
			print("NOT IMPLEMENTED")
			return

		self.topG.clear()
		self.topG.add_node(self.currentNodeValue())

		self.currentNodePerLevel[self.current_level] = self.currentNode
		
		self.current_level += 1
		self.currentNodeValue_list = self.getCurrentLevelNodeValueList()
		self.currentNode = 0 if len(self.currentNodeValue_list) != 0 else -1

		self.currentG.clear()
		if len(self.currentNodeValue_list) == 1:
			self.currentG.add_nodes_from(self.currentNodeValue_list)
		else:
			self.currentG.add_edges_from(self.getCurrentEdges())

		return


	def toTopLevel(self):
		if self.current_level == 0:
			print("topLevel: Error")
			return

		elif self.current_level == 1:
			self.topG.clear()

		else:
			self.topG.clear()
			parentNodeValueList = self.getLevelNodeValueList(self.current_level-2)
			parentNodeValue = parentNodeValueList[self.currentNodePerLevel[self.current_level-2]]
			self.topG.add_node(parentNodeValue)

		self.currentNodePerLevel[self.current_level] = self.currentNode

		self.current_level -= 1
		self.currentNode = self.currentNodePerLevel[self.current_level]

		self.redrawCurrent()
		
		return


class MemorySpace(MindMap):
	def __init__(self, axes):
		# super().__init__()
		self.currentG = nx.Graph()

		self.axes = axes

		self.level0 = {"root": []}
		self.levels = [self.level0]

		self.currentNodePerLevel = [-1]
		self.current_level = 0

		self.currentNodeValue_list = self.getCurrentLevelNodeValueList()
		self.currentNode = -1

		self.currentG.add_edges_from(self.getCurrentEdges())
		self.node_colors = ['skyblue' if not node == self.currentNodeValue() else 'yellow' for node in self.currentG.nodes()]

		self.updateCurrent()


	def updateCurrent(self):
		pos = self.getPos(self.currentNodeValue_list)
		self.node_colors = ['skyblue' if not node == self.currentNodeValue() else 'yellow' for node in self.currentG.nodes()]

		nx.draw_networkx_nodes(self.currentG, pos, ax=self.axes, node_color = self.node_colors, node_size = 2000)
		nx.draw_networkx_labels(self.currentG, pos, ax=self.axes, font_family = 'AppleGothic')
		nx.draw_networkx_edges(self.currentG, pos, ax=self.axes, edgelist=self.getCurrentEdges(), edge_color='white', arrows=False)
		self.axes.axis('off')
		print("MemorySpace", self.currentNodeValue_list, "currentNode: ", self.currentNode)

		return


	def addSpeech(self, newSpeech):
		if len(self.getCurrentLevelNodeValueList()) == 0:
			self.currentG.add_nodes_from([(newSpeech)])
			self.getCurrentLevelNodeValueList().append(newSpeech)
			self.currentNode = 0

		else:
			lastNodeValue = self.getCurrentLevelNodeValueList()[-1]
			self.getCurrentLevelNodeValueList().append(newSpeech)
			self.currentNode = len(self.getCurrentLevelNodeValueList()) - 1
			self.currentG.add_edges_from([(lastNodeValue, newSpeech)])

		return


	def popCurrentNode(self):
		currentNodeValueList = self.getCurrentLevelNodeValueList()
		try:
			currentNodeValue = currentNodeValueList[self.currentNode]
		except:
			return

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
		
		self.getCurrentLevelNodeValueList().pop(self.currentNode)
		self.currentG.remove_node(currentNodeValue)

		if leftNode	!= -1 and rightNode != -1:
			self.currentG.add_edge(leftNodeValue, rightNodeValue)

		self.currentNode = leftNode if leftNode != -1 else (rightNode-1)

		return currentNodeValue

