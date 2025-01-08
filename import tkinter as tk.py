import tkinter as tk
from tkinter import font

root = tk.Tk()
root.title('TESTING')

def funny():
    main = button.cget('text')
    new_text = 'button' if main == 'button' else 'funny'
    button.config(text= new_text)

def create_button():
    Custom_font = font.Font(family= 'airel',size = 42, weight= 'bold')
    global button
    button = tk.Button(root, text= ('button'), command = funny ,font=Custom_font, width=100,height=100)
    button.pack(side=tk.LEFT)

create_button()
root.mainloop()