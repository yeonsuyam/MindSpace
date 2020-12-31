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

	updateTop = False

	# Left hand for memoryspace
	# new node
	if event.key == 'k':
		swipeFlag = True
	elif event.key == 'u':
		newSpeech = speech.read()
		if newSpeech != "":
			memoryspace.addSpeech(newSpeech)
	elif event.key == 'j':
		memoryspace.toLeftNode()
	elif event.key == 'l':
		memoryspace.toRightNode()
	elif event.key == 'i':
		if swipeFlag:
			mindmap.addNodeToBottomLevel(memoryspace.popCurrentNode())
		else:
			mindmap.addNode(memoryspace.popCurrentNode())
			swipeFlag = False
		# else:
			# mindmap.addNode(memoryspace.popCurrentNode())
	# elif event.key == 'd':
		# memoryspace.addUpperNode()
	
	# Right hand for mindmaps
	if event.key == 's':
		mindmap.toLeftNode()
	elif event.key == 'f':
		mindmap.toRightNode()
	elif event.key == 'e':
		mindmap.bottomLevel()
		updateTop = True
	elif event.key == 'd':
		mindmap.toTopLevel()
		updateTop = True

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

# 	updateTop = False

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
# 		mindmap.bottomLevel()
# 		updateTop = True
# 	elif key == 'd':
# 		mindmap.toTopLevel()
# 		updateTop = True

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

# t = Thread(target=arduino, args=(fig, memoryspace_plt, mindmap_plt))
# t.daemon = False
# t.start()

# plt.gcf().canvas.mpl_connect('key_press_event', update)
plt.gcf().canvas.mpl_connect('key_press_event', keyboard_input)
plt.show(block=True)