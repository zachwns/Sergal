import tkinter as tk
from tkinter import ttk

main = tk.Tk()
main.title('idk bored')
text='button'
label = (0)

def thing(text):
    button = tk.Button(main,text=text,command=lambda: fun())
    button.pack(side=tk.LEFT)

def fun():
    global label
    label += 1
    print(label)
    if label == 2:
        tk.Label.destroy
        label - 2
        tk.Label(main,text='bye ig').pack()
    else:
        tk.Label(main,text='hello').pack()

thing(text)


main.mainloop()