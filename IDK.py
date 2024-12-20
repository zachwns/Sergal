import asyncio
import httpx
import tkinter as tk

def fetch_data():
    with httpx.Client() as client:
        response = client.get('https://svc.metrotransit.org/nextrip/routes')
        if response.status_code == 200:
            data = response.json()
            return(data)
        else:
            print('Failed to retrieve data:', response.status_code)

jsondata = fetch_data()


def on_click():
    label.config(text="Button clicked!")

# Create the main window
root = tk.Tk()
root.title("Simple GUI")

# Create a label and a button
label = tk.Label(root, text="Hello, World!")
label.pack(pady=10)

button = tk.Button(root, text=jsondata, command=on_click)
button.pack(pady=10)

# Run the main loop
root.mainloop() 