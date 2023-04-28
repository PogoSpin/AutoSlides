import pyautogui as pa           # run "pip install pyautogui" to intall
from aiAPI import *
import slideAPI
import ast
import time

def strToList(string):
    return ast.literal_eval(string.strip())          # removes \n and onverts string list into a list. Exp:  "[1, 2, 3]" becomes [1, 2, 3]

if __name__ == '__main__':
    with open('key.txt', 'r') as f:              #reads the openai key
        aiKey = f.readline().strip()

    print('\nAutoSlides Beta Test\n')

    topic = input('Presentation Topic: ')
    amountOfSlides = int(input('Amount of slides: '))



    genSlides = generate(f'I am making a powerpoint presentation about {topic}. Create a single line python list with the slide titles of each slide like this ["slide1", "slide2", "slide3"]. Create a max of {amountOfSlides} slides.', aiKey)
    genSlides = strToList(genSlides)

    print('This is the slides it will create: \n')                  # shows the slides it will make
    for slide in genSlides:
        print(slide)

    input('\nStart? ')

    time.sleep(2)
    slideText = ''
    for slide in genSlides:
        slideText = generate(f'I am making a powerpoint presentation about {topic}. Write the body for this slide title: {slide}.', aiKey).strip()
        slideAPI.createSlide(slide, slideText)
        print(f' \n {slide} \n {slideText}')