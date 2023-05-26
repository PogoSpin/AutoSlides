import pyautogui as pa           # run "pip install pyautogui" to intall

import customtkinter as ctk
import gptAPI as gpt
import ast, time, data, webbrowser
from slideAPI import Slides





def strToList(string):
    return ast.literal_eval(string.strip())          # removes \n and converts string list into a list. Exp:  "[1, 2, 3]" becomes [1, 2, 3]

    
    
# run

if __name__ == '__main__':
    class ScrollableEntryFrame(ctk.CTkScrollableFrame):                       # Generated slides scroll frame
        def __init__(self, master, item_list, command=None, **kwargs):
            super().__init__(master, **kwargs)

            self.command = command
            self.slideList = []
            self.slideTitles = item_list
            for item in item_list:
                self.add_item(item)

        def add_item(self, item):
            slide = ctk.CTkEntry(self, placeholder_text = item, width = 250)           # add generated slides
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
            result = []
            for id, slide in enumerate(self.slideList):    # loops over all the entries and adds the value to the return list, if nothing was changed it returns the placeholder text
                if slide.get() != '':
                    result.append(slide.get())
                else:
                    result.append(self.slideTitles[id])

            return result               # return the slide titles



    class App(ctk.CTk):
        def __init__(self):
            super().__init__()
            # app setup

            # Load Data
            self.aiKey = data.key                   # gets your api key from data.py
            self.positions = data.positions         # gets the button positions from data.py

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

    
            if self.aiKey == '':
                self.apiKey = ctk.CTkEntry(self, placeholder_text = 'API Key', width = 180)
            else:
                self.apiKey = ctk.CTkEntry(self, placeholder_text = self.aiKey, width = 180)


            self.apiKey.place(x = 50, y = 150)
            
            self.apiHelp = ctk.CTkButton(self, text = 'Help', width = 50, command = helpButton)
            self.apiHelp.place(x = 235, y = 150)




            def generateSlides():
                typedKey = self.apiKey.get()
                if typedKey != '':                    # only uses the typed key if you type something
                    with open('data.py', 'r+') as f:            # overwrites the saved api key with the new one
                        content = f.read()
                        # Replace the empty quotes with your text
                        new_content = content.replace(f"'{self.aiKey}'", f"'{typedKey}'")
                        f.seek(0)
                        f.write(new_content)
                        f.truncate()

                    self.aiKey = typedKey

                # Start of the generating process program.



                slides = Slides(self.positions[0], self.positions[1], self.positions[2])                  # creats a slides object and loads in the positios of the elements



                topic = self.topic.get()
                amountOfSlides = self.numOfSlides.get()
                wordLimit = self.wordAmount.get()

                
                
                # Safely generates the slides so if it doesn't succeed it will try again

                amountOfAttempts = 6     # How many more times it will attempt to generate text if it doesn't work the first time


                generatedSlides = None

                for i in range(amountOfAttempts):
                    succeded = False

                    try:
                        generatedSlides = gpt.generate(f'I am making a powerpoint presentation about {topic}. Create a single line python list with the slide titles of each slide like this ["slide1", "slide2", "slide3"]. Create a max of {amountOfSlides} slides.', self.aiKey)
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

                self.slidesFrame = ScrollableEntryFrame(self, label_text = 'Generated Slides', width = 250, height = 300, item_list = generatedSlides)
                self.slidesFrame.place(x = 700, y = 150)
                
                def createSlides():
                    # Creating position
                    if not self.positions:              # if there is no position data yet
                        self.positions = []

                        print('No position data found so it will be created now.\n')
                        print('Because this is the first time you lauched the program you will have to record the positions of all the google slide elements.')
                        print('Just follow the next instructions. \n')
                        print('Prepare you google slides presentation in the background with this terminal in front. ')
                        input('When ready, hover your mouse over the "add slide button" (the plus sign on the top left corner) and press enter.')

                        x, y = pa.position()                             #saves mouse pos
                        self.positions.append((x, y))

                        input('Done. Now when ready, hover your mouse over the title text box and press enter. (this is where the AI will type the title of each slide) ')

                        x, y = pa.position()                             #saves mouse pos
                        self.positions.append((x, y))

                        input('Done. Now last of all, when ready, hover your mouse over the main body text box and press enter. (this is where the AI will type in all the text for each slide) ')

                        x, y = pa.position()                             #saves mouse pos
                        self.positions.append((x, y))

                        print("\nPerfect, the positions have been saved to next time you won't have to do this again. ")

                        with open('data.py', 'r+') as f:
                            content = f.read()
                            # Replace the empty quotes with your text
                            new_content = content.replace("None", f"{self.positions}")
                            f.seek(0)
                            f.write(new_content)
                            f.truncate()

                        print('Now you can actually start. Press the create slides button again when you are ready. \n')
                    else:
                        generatedSlides = self.slidesFrame.get_checked_items()          # overwrites the generated slides with the changes the user made

                        for slide in generatedSlides:
                            slideText = None

                            for i in range(amountOfAttempts): # Attempts to generate slide text again if it fails
                                succeded = False

                                try:
                                    slideText = gpt.generate(f'I am making a powerpoint presentation about {topic}. Write the body for this slide title: {slide}. Use a max of {wordLimit} words. ', self.aiKey).strip()
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
                        

                self.createSlides = ctk.CTkButton(self, text = 'Create Slides', width = 350, height = 58, font = ('arial', 20), command = createSlides)
                self.createSlides.place(x = centerObj(350), y = 539)
            

            self.genSlides = ctk.CTkButton(self, text = 'Generate Slides', width = 350, command = generateSlides)
            self.genSlides.place(x = centerObj(350), y = 270)







    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('dark-blue')
    app = App()
    app.mainloop()
    






