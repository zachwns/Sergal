import tkinter as tk
from tkinter import font

def change_label():
    Label.config(text='Yaay the button was clicked')
    button.config(text="Clicked!!")
root = tk.Tk()
root.title('TESTING')

Label = tk.Label(root, text="Sad label")
Label.pack(pady=20)

button = tk.Button(root, text=('Click Me'), command = change_label)
button.pack()

root.mainloop()