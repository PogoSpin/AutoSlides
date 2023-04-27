import pyautogui as pa
import time
import slideAPI
from aiAPI import *
import ast

screenSize = (3840, 2400)

def strToList(string):
    return ast.literal_eval(string.strip())          # removes \n and onverts string list into a list. Exp:  "[1, 2, 3]" becomes [1, 2, 3]

if __name__ == '__main__':
    with open('key.txt', 'r') as f:              #reads the openai key
        aiKey = f.readline().strip()

    print('\n AutoSlides Beta Test')

    topic = input('Presentation Topic: ')
    slidesNumber = int(input('Amount of slides: '))


    time.sleep(2)

    slides = generate(f'I am making a powerpoint presentation about {topic}. Create a single line python list with the slide titles of each slide. Create a max of {slidesNumber} slides.', aiKey)
    slides = strToList(slides)

    print('This is the slides it will create: \n')                  # shows the slides it will make
    for slide in slides:
        print(slide)

    slideText = ''
    for slide in slides:
        slideText = generate(f'I am making a powerpoint presentation about {topic}. Write the body for this slide title: {slide}.', aiKey).strip()
        slideAPI.createSlide(slide, slideText)
        print(f' \n {slide} \n {slideText}')

# while True:
#     print(pa.position())