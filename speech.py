import math

class Speech:
	def __init__(self):
		self.f = open("./input.txt", 'r')

	def read(self):
		newWordList = []
		line = self.f.readline().strip()
		wordList = line.split(" ")

		for i in range(math.ceil(len(wordList)/3.0)):
			if i == 0:
				newWordList += (wordList[i*3:(i+1)*3])
			else:
				newWordList += (["\n"] + wordList[i*3:(i+1)*3])

		return ' '.join(newWordList)