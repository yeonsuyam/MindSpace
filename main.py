import matplotlib as mpl
import matplotlib.pyplot as plt

from speech import Speech
from mindmap import MindMap, MemorySpace

from threading import *
from time import sleep
import serial


# left hand: sfed, r
# right hand: jlik, u
def keyboard_input(event):
	global mindmap
	global memoryspace

	updateTop = False

	# Left hand for memoryspace
	# new node
	if event.key == 'u':
		newSpeech = speech.read()
		if newSpeech != "":
			memoryspace.addSpeech(newSpeech)
	if event.key == 'j':
		memoryspace.left()
	elif event.key == 'l':
		memoryspace.right()
	elif event.key == 'i':
		mindmap.addNode(memoryspace.popCurrentNode())
	# elif event.key == 'd':
		# memoryspace.addUpperNode()
	
	# Right hand for mindmaps
	if event.key == 's':
		mindmap.left()
	elif event.key == 'f':
		mindmap.right()
	elif event.key == 'e':
		mindmap.bottomLevel()
		updateTop = True
	elif event.key == 'd':
		mindmap.topLevel()
		updateTop = True

	plt.clf()

	memoryspace_plt = plt.subplot(1, 2, 2)
	memoryspace_plt.set_xlim(-3, 3)
	memoryspace_plt.set_ylim(-7, 7)
	memoryspace.updateCurrent()

	mindmap_plt = plt.subplot(1, 2, 1)
	mindmap_plt.set_xlim(-3, 3)
	mindmap_plt.set_ylim(-7, 7)
	mindmap.updateCurrent()
	mindmap.updateTop()		

	plt.draw()


def arduino():
	ser = serial.Serial(
		# TODO: Check port, baudrate
		# port='/dev/cu.usbmodem72758601 Serial (Teensy 3.2)',
		port='/dev/cu.usbmodem72758601',
		# port='/dev/cu.usbmodem72758601 (Teensy) Serial',
		baudrate=9600,
	)

	while True:
		if ser.readable():
			res = ser.readline()
			print(res.decode()[:len(res)-1])

	print('Finish touch input')
	return


Stopped = False
t = Thread(target=arduino, args=())
t.start()

speech = Speech()

# Disable keyboard shortcuts in Matplotlib
# print(plt.rcParams)
plt.rcParams['keymap.fullscreen'] = 'ctrl+f'
plt.rcParams['keymap.save'] = 'ctrl+s'
mpl.rcParams['axes.unicode_minus'] = False

memoryspace_plt = plt.subplot(1, 2, 2)
memoryspace_plt.set_ylim(5, -5)
memoryspace = MemorySpace()

mindmap_plt = plt.subplot(1, 2, 1)
mindmap_plt.set_ylim(5, -5)
mindmap = MindMap()

plt.gcf().canvas.mpl_connect('key_press_event', keyboard_input)
plt.show()