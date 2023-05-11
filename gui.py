import customtkinter as ctk
import webbrowser

class ScrollableEntryFrame(ctk.CTkScrollableFrame):
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

        self.genSlides = ctk.CTkButton(self, text = 'Generate Slides', width = 350)
        self.genSlides.place(x = centerObj(350), y = 250)



        # Left info section
        self.info = ctk.CTkLabel(self, text = 'Info', font = ('arial', 30))
        self.info.place(x = 125, y = 35)

        self.apiKey = ctk.CTkEntry(self, placeholder_text = 'API Key', width = 180)
        self.apiKey.place(x = 50, y = 150)

        self.apiHelp = ctk.CTkButton(self, text = 'Help', width = 50, command = helpButton)
        self.apiHelp.place(x = 235, y = 150)



        # Right Side

        # self.slidesFrame = ctk.CTkScrollableFrame(self, width = 250, height = 300, label_text = 'Generated Slides')
        self.slidesFrame = ScrollableEntryFrame(self, label_text = 'Generated Slides', width = 250, height = 300, item_list=[f'item {i}' for i in range(50)])
        self.slidesFrame.place(x = 700, y = 150)




# run

if __name__ == '__main__':
    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('dark-blue')
    app = App()
    app.mainloop()