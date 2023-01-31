import pyautogui, sys

pyautogui.keyDown('w')  # hold down the shift key
pyautogui.press('space')     # press the left arrow key
pyautogui.press('space')     # press the left arrow key
pyautogui.keyUp('w')    # release the shift key

pyautogui.moveTo(100, 200, 2)