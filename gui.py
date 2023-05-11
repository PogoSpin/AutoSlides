import customtkinter as ctk
import webbrowser

class ScrollableEntryFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.checkbox_list = []
        for i, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        checkbox = ctk.CTkCheckBox(self, text=item)
        if self.command is not None:
            checkbox.configure(command=self.command)
        checkbox.grid(row=len(self.checkbox_list), column=0, pady=(0, 10))
        self.checkbox_list.append(checkbox)

    def remove_item(self, item):
        for checkbox in self.checkbox_list:
            if item == checkbox.cget("text"):
                checkbox.destroy()
                self.checkbox_list.remove(checkbox)
                return

    def get_checked_items(self):
        return [checkbox.cget("text") for checkbox in self.checkbox_list if checkbox.get() == 1]

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
        title = ctk.CTkLabel(self, text = 'Auto Slides', font = ('arial', 40))
        title.grid(pady = 30)

        topic = ctk.CTkEntry(self, placeholder_text = 'Presentation Topic', width = 350)
        topic.place(x = centerObj(350), y = 150)

        numOfSlides = ctk.CTkEntry(self, placeholder_text = 'Amount of Slides', width = 350)
        numOfSlides.place(x = centerObj(350), y = 190)

        genSlides = ctk.CTkButton(self, text = 'Generate Slides', width = 350)
        genSlides.place(x = centerObj(350), y = 250)



        # Left info section
        info = ctk.CTkLabel(self, text = 'Info', font = ('arial', 30))
        info.place(x = 125, y = 35)

        apiKey = ctk.CTkEntry(self, placeholder_text = 'API Key', width = 180)
        apiKey.place(x = 50, y = 150)

        apiHelp = ctk.CTkButton(self, text = 'Help', width = 50, command = helpButton)
        apiHelp.place(x = 235, y = 150)



        # Right Side

        slidesFrame = ctk.CTkScrollableFrame(self, width = 250, height = 300, label_text = 'Generated Slides')
        slidesFrame.place(x = 700, y = 150)




# run

if __name__ == '__main__':
    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('dark-blue')
    app = App()
    app.mainloop()