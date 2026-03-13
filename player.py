import time

from pynput.keyboard import Listener, Controller, Key

keyboard = Controller()

shiftMap = { "!": "1", "@": "2", "#": "3", "$": "4", "%": "5", "^": "6", "&": "7", "*": "8", "(": "9", ")": "0" }

def needsShift(key: str):
	return key.lower() if key.isupper() else shiftMap.get(key, None)

def pressOnce(key):
	shift = needsShift(key)
	if shift is None:
		keyboard.press(key)
		keyboard.release(key)
	else:
		keyboard.press(Key.shift)
		keyboard.press(shift)
		keyboard.release(shift)
		keyboard.release(Key.shift)

def play(seq: str):
	tokens = seq.split(" ")

	running = True
	end = len(tokens) - 1

	def on_press(key):
		nonlocal running
		if key == Key.esc:
			running = False
			return False

	listener = Listener(on_press=on_press)
	listener.start()
	
	i = 0
	while running:
		token = tokens[i]
		if token.startswith("[") and token.endswith("]"):
			keys = token[1:-1]
			for k in keys:
				pressOnce(k)
		elif token.startswith("(") and token.endswith(")"):
			wait = float(token[1:-1])
			time.sleep(wait)
		else:
			pressOnce(token)

		i += 1
		if i > end: i = 0

		time.sleep(0.01)

	del listener
