import customtkinter as ctk

# window setup
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

window = ctk.CTk()
window.title('Auto Slides')
window.geometry('500x300')

window.grid_columnconfigure(0, weight=1)       # makes everything centered??    https://customtkinter.tomschimansky.com/tutorial/

# widgets
label = ctk.CTkLabel(window, text = 'Auto Slides', font = ('arial', 40))
label.grid(pady = 20)

topic = ctk.CTkEntry(window, placeholder_text = 'Presentation Topic')
topic.grid(pady = 15, padx = 60, sticky = 'ew')

topic = ctk.CTkEntry(window, placeholder_text = 'Amount of Slides')
topic.grid(pady = 0, padx = 60, sticky = 'ew')

button = ctk.CTkButton(window, text = 'Generate Slides')
button.grid(pady = 40, padx = 60, sticky = 'ew')


# run
window.mainloop()