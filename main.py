import matplotlib as mpl
import matplotlib.pyplot as plt

from speech import Speech
from mindmap import MindMap, MemorySpace

from threading import *
from time import sleep
import serial
import keyboard


def update(event):
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


# left hand: sfed, r
# right hand: jlik, u
def keyboard_input(key, fig, memoryspace_plt, mindmap_plt):
	global mindmap
	global memoryspace

	updateTop = False

	# Left hand for memoryspace
	# new node
	if key == 'u':
		newSpeech = speech.read()
		if newSpeech != "":
			memoryspace.addSpeech(newSpeech)
	if key == 'j':
		memoryspace.left()
	elif key == 'l':
		memoryspace.right()
	elif key == 'i':
		mindmap.addNode(memoryspace.popCurrentNode())
	# elif event.key == 'd':
		# memoryspace.addUpperNode()
	
	# Right hand for mindmaps
	if key == 's':
		mindmap.left()
	elif key == 'f':
		mindmap.right()
	elif key == 'e':
		mindmap.bottomLevel()
		updateTop = True
	elif key == 'd':
		mindmap.topLevel()
		updateTop = True

	keyboard.press_and_release('enter') # To call update function on main thread
	
	return


def arduino(fig, memoryspace_plt, mindmap_plt):
	ser = serial.Serial(
		# TODO: Check port, baudrate
		# port='/dev/cu.usbmodem72758601 Serial (Teensy 3.2)',
		port='/dev/cu.usbmodem72758601',
		# port='/dev/cu.usbmodem72758601 (Teensy) Serial',
		baudrate=9600,
	)

	# while True:
	# 	if ser.readable():
	# 		print("readable")
	# 		res = ser.readline()
	# 		res = res.decode()[:len(res)-1]
	# 		keyboard_input('u', fig, memoryspace_plt, mindmap_plt)
			
	for i in range(3):
		keyboard_input('u', fig, memoryspace_plt, mindmap_plt)
		sleep(2)


	print('Finish touch input')
	return


speech = Speech()

# Disable keyboard shortcuts in Matplotlib
# print(plt.rcParams)
plt.rcParams['keymap.fullscreen'] = 'ctrl+f'
plt.rcParams['keymap.save'] = 'ctrl+s'
mpl.rcParams['axes.unicode_minus'] = False

fig = plt.figure()
memoryspace_plt = fig.add_subplot(1, 2, 2)
memoryspace_plt.set_ylim(5, -5)
memoryspace = MemorySpace()

mindmap_plt = fig.add_subplot(1, 2, 1)
mindmap_plt.set_ylim(5, -5)
mindmap = MindMap()

Stopped = False
t = Thread(target=arduino, args=(fig, memoryspace_plt, mindmap_plt))
t.daemon = False
t.start()

plt.gcf().canvas.mpl_connect('key_press_event', update)
plt.show(block=True)