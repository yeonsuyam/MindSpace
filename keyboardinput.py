import matplotlib as mpl
import matplotlib.pyplot as plt
from threading import *
import keyboard
from time import sleep
from pynput.keyboard import Key, Controller


for i in range(5):
	sleep(2)
	keyboard.press_and_release('shift+s, space')
	keyboard.send('u')
	# keyboard.write('u')
	# keyboard.press_and_release('ctrl+tab')
