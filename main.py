import pyautogui as pa           # run "pip install pyautogui" to intall
import customtkinter as ctk
import gptAPI as gpt
import ast, time, data, webbrowser
from slideAPI import Slides





def strToList(string):
    return ast.literal_eval(string.strip())          # removes \n and converts string list into a list. Exp:  "[1, 2, 3]" becomes [1, 2, 3]

    
    
# run

if __name__ == '__main__':

    # Load Data
    aiKey = data.key                   # gets your api key from data.py
    positions = data.positions         # gets the button positions from data.py



    class ScrollableEntryFrame(ctk.CTkScrollableFrame):                       # Generated slides scroll frame
        def __init__(self, master, item_list, command=None, **kwargs):
            super().__init__(master, **kwargs)

            self.command = command
            self.slideList = []
            for i, item in enumerate(item_list):
                self.add_item(item)

        def add_item(self, item):
            slide = ctk.CTkEntry(self, placeholder_text = item)           # add generated slides
            if self.command is not None:
                slide.configure(command=self.command)
            slide.grid(row=len(self.slideList), column=0, pady=(0, 10))
            self.slideList.append(slide)

        def remove_item(self, item):
            for slide in self.slideList:
                if item == slide.cget('text'):
                    slide.destroy()
                    self.slideList.remove(slide)
                    return

        def get_checked_items(self):
            return [slide.cget('text') for slide in self.slideList if slide.get() == 1]



    class App(ctk.CTk):
        def __init__(self):
            super().__init__()
            # app setup

            self.size = (1000, 700)

            self.title('Auto Slides')
            self.geometry(f'{self.size[0]}x{self.size[1]}')

            self.resizable(False, False)
            self.grid_columnconfigure(0, weight=1)       # makes everything centered??    https://customtkinter.tomschimansky.com/tutorial/

            def centerObj(width):
                return (self.size[0]/2) - (width/2)


            def helpButton():
                webbrowser.open('https://platform.openai.com/account/api-keys')

            # widgets

            # Main center part
            self.title = ctk.CTkLabel(self, text = 'Auto Slides', font = ('arial', 40))
            self.title.grid(pady = 30)

            self.topic = ctk.CTkEntry(self, placeholder_text = 'Presentation Topic', width = 350)
            self.topic.place(x = centerObj(350), y = 150)

            self.numOfSlides = ctk.CTkEntry(self, placeholder_text = 'Amount of Slides', width = 350)
            self.numOfSlides.place(x = centerObj(350), y = 190)

            self.wordAmount = ctk.CTkEntry(self, placeholder_text = 'Words per Slide', width = 350)
            self.wordAmount.place(x = centerObj(350), y = 230)


            # Left info section
            self.info = ctk.CTkLabel(self, text = 'Info', font = ('arial', 30))
            self.info.place(x = 125, y = 35)


            if aiKey == '':
                self.apiKey = ctk.CTkEntry(self, placeholder_text = 'API Key', width = 180)
            else:
                self.apiKey = ctk.CTkEntry(self, placeholder_text = aiKey, width = 180)


            self.apiKey.place(x = 50, y = 150)
            
            self.apiHelp = ctk.CTkButton(self, text = 'Help', width = 50, command = helpButton)
            self.apiHelp.place(x = 235, y = 150)




            def generateSlides():
                self.slidesFrame = ScrollableEntryFrame(self, label_text = 'Generated Slides', width = 250, height = 300, item_list=[f'item {i}' for i in range(50)])
                self.slidesFrame.place(x = 700, y = 150)


                # TODO
                aiKey = self.apiKey.get()
                
                # with open('data.py', 'r+') as f:            # TODO           add overwrite if api key is not none and if api key is saved then display as placeholder text
                #     content = f.read()
                #     # Replace the empty quotes with your text
                #     new_content = content.replace("''", f"'{aiKey}'")
                #     f.seek(0)
                #     f.write(new_content)
                #     f.truncate()




                # Start of the generating process program.



                slides = Slides(positions[0], positions[1], positions[2])                  # creats a slides object and loads in the positios of the elements



                topic = self.topic.get()
                amountOfSlides = self.numOfSlides.get()
                wordLimit = self.wordAmount.get()

                
                
                # Safely generates the slides so if it doesn't succeed it will try again

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

            

            self.genSlides = ctk.CTkButton(self, text = 'Generate Slides', width = 350, command = generateSlides)
            self.genSlides.place(x = centerObj(350), y = 250)







    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('dark-blue')
    app = App()
    app.mainloop()


    # # Creating position
    # if not positions:              # if there is no position data yet
    #     positions = []

    #     print('No position data found so it will be created now.\n')
    #     print('Because this is the first time you lauched the program you will have to record the positions of all the google slide elements.')
    #     print('Just follow the next instructions. \n')
    #     print('Prepare you google slides presentation in the background with this terminal in front. ')
    #     input('When ready, hover your mouse over the "add slide button" (the plus sign on the top left corner) and press enter.')

    #     x, y = pa.position()                             #saves mouse pos
    #     positions.append((x, y))

    #     input('Done. Now when ready, hover your mouse over the title text box and press enter. (this is where the AI will type the title of each slide) ')

    #     x, y = pa.position()                             #saves mouse pos
    #     positions.append((x, y))

    #     input('Done. Now last of all, when ready, hover your mouse over the main body text box and press enter. (this is where the AI will type in all the text for each slide) ')

    #     x, y = pa.position()                             #saves mouse pos
    #     positions.append((x, y))

    #     print("\nPerfect, the positions have been saved to next time you won't have to do this again. ")
    #     print('Now you can actually start. \n')

    #     with open('data.py', 'r+') as f:
    #         content = f.read()
    #         # Replace the empty quotes with your text
    #         new_content = content.replace("None", f"{positions}")
    #         f.seek(0)
    #         f.write(new_content)
    #         f.truncate()





