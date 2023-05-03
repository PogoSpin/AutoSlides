import tkinter as tk
from customtkinter import *
 
class App(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
        self.main_frame = CTkFrame(self)
        self.main_frame.pack(expand=True, fill=tk.BOTH)
 
app = App()
app.geometry('1920x1080')
app.mainloop()