import pyautogui as pa           # run "pip install pyautogui" to intall
import gptAPI as gpt
import ast, time, data
from slideAPI import Slides

def strToList(string):
    return ast.literal_eval(string.strip())          # removes \n and converts string list into a list. Exp:  "[1, 2, 3]" becomes [1, 2, 3]

if __name__ == '__main__':

    # Load Data
    aiKey = data.key                   # gets your api key from data.py
    positions = data.positions         # gets the button positions from data.py


    print('\nAutoSlides Beta Test\n')

    # Create Data
    if aiKey == '':
        while aiKey == '':
            print('You have not yet typed in your API key. You can get yours through "https://platform.openai.com/account/api-keys".')
            aiKey = input('API Key: ')
        
        with open('data.py', 'r+') as f:
            content = f.read()
            # Replace the empty quotes with your text
            new_content = content.replace("''", f"'{aiKey}'")
            f.seek(0)
            f.write(new_content)
            f.truncate()

        print()

    # Creating position
    if not positions:              # if there is no position data yet
        positions = []

        print('No position data found so it will be created now.\n')
        print('Because this is the first time you lauched the program you will have to record the positions of all the google slide elements.')
        print('Just follow the next instructions. \n')
        print('Prepare you google slides presentation in the background with this terminal in front. ')
        input('When ready, hover your mouse over the "add slide button" (the plus sign on the top left corner) and press enter.')

        x, y = pa.position()                             #saves mouse pos
        positions.append((x, y))

        input('Done. Now when ready, hover your mouse over the title text box and press enter. (this is where the AI will type the title of each slide) ')

        x, y = pa.position()                             #saves mouse pos
        positions.append((x, y))

        input('Done. Now last of all, when ready, hover your mouse over the main body text box and press enter. (this is where the AI will type in all the text for each slide) ')

        x, y = pa.position()                             #saves mouse pos
        positions.append((x, y))

        print("\nPerfect, the positions have been saved to next time you won't have to do this again. ")
        print('Now you can actually start. \n')

        with open('data.py', 'r+') as f:
            content = f.read()
            # Replace the empty quotes with your text
            new_content = content.replace("None", f"{positions}")
            f.seek(0)
            f.write(new_content)
            f.truncate()






    # Start of actual program. The rest above was setup



    slides = Slides(positions[0], positions[1], positions[2])                  # creats a slides object and loads in the positios of the elements



    topic = input('Presentation Topic: ')
    amountOfSlides = int(input('Amount of slides: '))
    wordLimit = int(input('Word amount per slide: '))

    
    
    # Safely generates the slides so if it doesn't succed it will try again

    amountOfAttempts = 6     # How many more times it will attempt to generate text if it doesn't work the first time


    generatedSlides = None

    for i in range(amountOfAttempts):
        succeded = False

        try:
            generatedSlides = gpt.generate(f'I am making a powerpoint presentation about {topic}. Create a single line python list with the slide titles of each slide like this ["slide1", "slide2", "slide3"]. Create a max of {amountOfSlides} slides.', aiKey)
            succeded = True
        except:
            print(f'Failed to generate slide titles on try {i+1}. Trying again in {i**2} second\s... ')
            time.sleep(i**2)

        if succeded:
            break
    
    if succeded:
        print()
    else:
        print(f'\nFailed to generate slide titles after {amountOfAttempts + 1} attempts. ')
        quit()



    generatedSlides = strToList(generatedSlides)

    print('These is the slides it will create: \n')                  # shows the slides it will make
    for slide in generatedSlides:
        print(slide)

    input('\nStart? ')

    time.sleep(2)
    for slide in generatedSlides:
        slideText = None

        for i in range(amountOfAttempts): # Attempts to generate slide text again if it fails
            succeded = False

            try:
                slideText = gpt.generate(f'I am making a powerpoint presentation about {topic}. Write the body for this slide title: {slide}. Use a max of {wordLimit} words. ', aiKey).strip()
                succeded = True
            except:
                print(f'Failed to generate slide text on try {i+1}. Trying again in {i**2} second\s... ')
                time.sleep(i**2)

            if succeded:
                break
    
        if succeded:
            slides.createNewSlide(slide, slideText)
        else:
            print(f'\nFailed to generate slide content after {amountOfAttempts} attempts. ')
            quit()


    print('\nTask Completed! ')