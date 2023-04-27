import pyautogui as pa

class Positions:
    title = (1138, 845)
    text = (1476, 1154)
    newSlide = (100, 467)

def createSlide(title, text):
    pa.moveTo(Positions.newSlide[0], Positions.newSlide[1], 1)
    pa.click()
    pa.moveTo(Positions.title[0], Positions.title[1], 1)
    pa.click()
    pa.write(title, 0.01)
    pa.moveTo(Positions.text[0], Positions.text[1], 1)
    pa.click()
    pa.write(text, 0.01)