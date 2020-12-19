class Speech:
	def __init__(self):
		self.f = open("./input.txt", 'r')

	def read(self):
		line = self.f.readline()
		print(line)
		return line