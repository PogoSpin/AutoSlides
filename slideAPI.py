import pyautogui as pa

class Slides:
    mouseMoveSpeed = 0.5
    def __init__(self, newSlidePos, titlePos, textPos):
        self.title = titlePos                   # (x, y) pos of the title box
        self.text = textPos                     # (x, y) pos of the main text box
        self.newSlide = newSlidePos             # (x, y) pos of the new slide button

    def createNewSlide(self, title, text):
        pa.moveTo(self.newSlide[0], self.newSlide[1], Slides.mouseMoveSpeed)
        pa.click()

        pa.moveTo(self.title[0], self.title[1], Slides.mouseMoveSpeed)
        pa.click()

        pa.write(title, 0.01)

        pa.moveTo(self.text[0], self.text[1], Slides.mouseMoveSpeed)
        pa.click()

        pa.write(text, 0.01)