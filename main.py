import matplotlib as mpl
import matplotlib.pyplot as plt

from speech import Speech
from mindmap import MindMap, MemorySpace

from threading import *
from time import sleep
import serial
import keyboard


# def update(event):
# 	memoryspace_plt.clear()
# 	memoryspace_plt.set_xlim(-3, 3)
# 	memoryspace_plt.set_ylim(-7, 7)
# 	memoryspace_plt.plot()
# 	memoryspace.updateCurrent(memoryspace_plt)


# 	mindmap_plt.clear()
# 	mindmap_plt.set_xlim(-3, 3)
# 	mindmap_plt.set_ylim(-7, 7)
# 	mindmap.updateCurrent()
# 	mindmap.updateTop()

# 	fig.canvas.draw_idle()


def keyboard_input(event):
	global mindmap
	global memoryspace
	global swipeFlag
	global moveNodeFlag

	print()

	# Right hand for MemorySpace
	if event.key == 'k':
		swipeFlag = True
	elif event.key == 'u':
		print("u")
		newSpeech = speech.read()
		if newSpeech != "":
			memoryspace.addSpeech(newSpeech)
	elif event.key == 'j':
		if swipeFlag:
			print("kj")
			mindmap.addNode(memoryspace.popCurrentNode())
			swipeFlag = False
		else:
			print("j")
			memoryspace.toLeftNode()
	elif event.key == 'l':
		print("i")
		memoryspace.toRightNode()
	elif event.key == 'i':
		if swipeFlag:
			print("ki")
			mindmap.addNodeToBottomLevel(memoryspace.popCurrentNode())
			swipeFlag = False
	
	# Left hand for MindMaps
	if event.key == 'd': 
		moveNodeFlag = True
	elif event.key == 's':
		if moveNodeFlag:
			print("ds")
			mindmap.moveNodeToLeft()
			moveNodeFlag = False
		else:
			print("s")
			mindmap.toLeftNode()
	elif event.key == 'f':
		if moveNodeFlag:
			print("df")
			mindmap.moveNodeToRight()
			moveNodeFlag = False
		else:
			print("f")
			mindmap.toRightNode()
	elif event.key == 'e':
		print("e")
		mindmap.toTopLevel()
	elif event.key == 'c':
		print("c")
		mindmap.toBottomLevel()

	memoryspace_plt.clear()
	memoryspace_plt.set_xlim(-3, 3)
	memoryspace_plt.set_ylim(-7, 7)
	memoryspace_plt.plot()
	memoryspace.updateCurrent(memoryspace_plt)

	mindmap_plt.clear()
	mindmap_plt.set_xlim(-3, 3)
	mindmap_plt.set_ylim(-7, 7)
	mindmap.updateCurrent()
	mindmap.updateTop()

	fig.canvas.draw_idle()
	
	return


# def keyboard_input(key, fig, memoryspace_plt, mindmap_plt):
# 	global mindmap
# 	global memoryspace

# 	# Left hand for memoryspace
# 	# new node
# 	if key == 'u':
# 		newSpeech = speech.read()
# 		if newSpeech != "":
# 			memoryspace.addSpeech(newSpeech)
# 	if key == 'j':
# 		memoryspace.toLeftNode()
# 	elif key == 'l':
# 		memoryspace.toRightNode()
# 	elif key == 'i':
# 		mindmap.addNode(memoryspace.popCurrentNode())
# 	# elif event.key == 'd':
# 		# memoryspace.addUpperNode()
	
# 	# Right hand for mindmaps
# 	if key == 's':
# 		mindmap.toLeftNode()
# 	elif key == 'f':
# 		mindmap.toRightNode()
# 	elif key == 'e':
# 		mindmap.toBottomLevel()
# 	elif key == 'd':
# 		mindmap.toTopLevel()

# 	keyboard.press_and_release('enter') # To call update function on main thread
	
# 	return


def arduino(fig, memoryspace_plt, mindmap_plt):
	# ser = serial.Serial(
	# 	port='/dev/cu.usbmodem72758601',
	# 	baudrate=9600,
	# )

	# while True:
	# 	if ser.readable():
	# 		print("readable")
	# 		res = ser.readline()
	# 		res = res.decode()[:len(res)-1]
	# 		keyboard_input('u', fig, memoryspace_plt, mindmap_plt)
			
	return


speech = Speech()

# Disable keyboard shortcuts in Matplotlib
# print(plt.rcParams)
plt.rcParams['keymap.fullscreen'] = 'ctrl+f'
plt.rcParams['keymap.save'] = 'ctrl+s'
mpl.rcParams['axes.unicode_minus'] = False

fig = plt.figure()
memoryspace_plt = fig.add_subplot(1, 2, 2)
memoryspace_plt.set_xlim(-3, 3)
memoryspace_plt.set_ylim(-7, 7)
memoryspace = MemorySpace()

mindmap_plt = fig.add_subplot(1, 2, 1)
mindmap_plt.set_xlim(-3, 3)
mindmap_plt.set_ylim(-7, 7)
mindmap = MindMap()

swipeFlag = False
moveNodeFlag = False

# t = Thread(target=arduino, args=(fig, memoryspace_plt, mindmap_plt))
# t.daemon = False
# t.start()

# plt.gcf().canvas.mpl_connect('key_press_event', update)
plt.gcf().canvas.mpl_connect('key_press_event', keyboard_input)
plt.show(block=True)