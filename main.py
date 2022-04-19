import time
import pynput.keyboard as keyboard
import threading
import pyautogui
import os


kbd = keyboard.Controller()


press_time = None
query = ''


pressed = False
last_press = None

morse_code = {'.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W',
              '-..-': 'X', '-.--': 'Y', '--..': 'Z', '.----': '1', '..---': '2', '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9', '-----': '0', '--..--': ', ', '.-.-.-': '.', '..--..': '?', '-..-.': '/', '-....-': '-', '-.--.': '(', '-.--.-': ')', '......': ' ', '---...': 'backspace', '...---': 'return','......-':'quit'}

def translate_loop():
    global query
    while True:
        if last_press != None:
            DIFF = time.time() - last_press
            if DIFF > 1 and pressed == False:
                if query in morse_code:
                    for i in query:
                        kbd.press(keyboard.Key.backspace)
                        kbd.release(keyboard.Key.backspace)

                    dec = morse_code[query]
                    query = ''
                    if dec == ' ':
                        kbd.press(keyboard.Key.space)
                        kbd.release(keyboard.Key.space)
                        continue

                    if dec == 'backspace':
                        kbd.press(keyboard.Key.backspace)
                        kbd.release(keyboard.Key.backspace)
                        continue

                    if dec == 'return':
                        kbd.press(keyboard.Key.enter)
                        kbd.release(keyboard.Key.enter)
                        continue

                    if dec == 'quit':
                        os._exit(0)

                    pyautogui.typewrite(dec)

        time.sleep(0.2)


def on_press(x):
    global press_time
    global pressed

    if x == keyboard.Key.cmd:
        if not pressed:
            press_time = time.time()

    pressed = True
    if x == keyboard.Key.esc:
        os._exit(0)


def on_release(x):
    global pressed
    global query
    global last_press

    pressed = False
    if x == keyboard.Key.cmd:
        held_time = time.time() - press_time

        if held_time > 0.3:
            query += '-'
            kbd.press('-')
            kbd.release('-')
        else:
            query += '.'
            kbd.press('.')
            kbd.release('.')
    elif x == keyboard.Key.shift_r:
        query = ''

    last_press = time.time()

threading.Thread(target=translate_loop).start()
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
