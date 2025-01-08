import tkinter as tk
from tkinter import ttk
import asyncio
import httpx
from plyer import notification
import threading

# Dictionary to keep track of auto-update flags for each stop
auto_update_flags = {}
# Global variable to store the latest departure
latest_departure = None

# Asynchronous function to fetch data from the Metro Transit API for a given stop_id
async def fetch_data(stop_id):
    async with httpx.AsyncClient() as client:
        url = f'https://svc.metrotransit.org/nextrip/{stop_id}'
        response = await client.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Failed to retrieve data for stop_id {stop_id}:', response.status_code)
            return []

# Function to update the UI with fetched data and update the global variable 'latest_departure'
def update_ui(data, stop_id):
    global latest_departure  # Use the global variable
    print(f"Updating UI with fetched data for stop_id {stop_id}")
    tree.delete(*tree.get_children())  # Clear the Treeview
    if isinstance(data, list) and data:
        latest_departure = data[0]  # Update the global variable with the first departure
        for item in data:
            departure_text = item.get('departure_text', 'N/A')
            route_id = item.get('route_id', 'N/A')
            direction = item.get('direction_text', 'N/A')
            # Insert the fetched data into the Treeview
            tree.insert('', 'end', text=route_id, values=(departure_text, direction))
            # Show notification if the departure time is '5 Min'
            if departure_text == '5 Min':
                show_notification(route_id, direction, departure_text)

# Function to show a notification with route details
def show_notification(route_id, direction, departure_text):
    title = "Metro Transit Notification"
    message = f"Route {route_id} is due in {departure_text}"
    # Use a separate thread to show the notification
    threading.Thread(target=lambda: notification.notify(
        title=title,
        message=message,
        timeout=5
    )).start()

# Function to start fetching data for a given stop_id and update the UI
def start_fetching(stop_id):
    def fetch_and_update():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        print(f"Starting fetch for {stop_id}")
        data = loop.run_until_complete(fetch_data(stop_id))
        update_ui(data.get('departures', []), stop_id)
        if auto_update_flags.get(stop_id, False):
            print(f"Scheduling next fetch for {stop_id}")
            # Schedule the next fetch after 30 seconds if auto-update is enabled
            root.after(30000, lambda: start_fetching(stop_id))

    # Use a separate thread to fetch data
    threading.Thread(target=fetch_and_update).start()

# Event handler for double-click on Treeview item to show details in a new window
def on_item_click(event):
    item_id = tree.selection()[0]
    item = tree.item(item_id)
    show_details(item['text'], item['values'])

# Function to show details of the selected route in a new window
def show_details(route_id, details):
    detail_window = tk.Toplevel(root)
    detail_window.title(f"Details for Route {route_id}")

    tk.Label(detail_window, text=f"Route ID: {route_id}").pack()
    tk.Label(detail_window, text=f"Due Time: {details[0]}").pack()
    tk.Label(detail_window, text=f"Direction: {details[1]}").pack()
    tk.Label(detail_window, text="Additional info here...").pack()

    tk.Button(detail_window, text="Close", command=detail_window.destroy).pack()

# Function to start auto-update for a given stop_id
def start_auto_update(stop_id):
    auto_update_flags[stop_id] = True
    start_fetching(stop_id)

# Function to stop auto-update for a given stop_id
def stop_auto_update(stop_id):
    auto_update_flags[stop_id] = False

# Initialize the main window
root = tk.Tk()
root.title('Metro Transit Data')

# Create a Treeview widget to display route data
tree = ttk.Treeview(root)
tree['columns'] = ('departure_text', 'direction')
tree.column('#0', width=100, minwidth=100)
tree.column('departure_text', width=100, minwidth=100)
tree.column('direction', width=200, minwidth=200)

tree.heading('#0', text='Route ID', anchor=tk.W)
tree.heading('departure_text', text='Due Time', anchor=tk.W)
tree.heading('direction', text='Direction', anchor=tk.W)

tree.pack(side='top', fill='both', expand=True)

# Bind double-click event to show item details
tree.bind('<Double-1>', on_item_click)

# Function to create buttons for fetching data for specific stops
def create_button(stop_id, text, auto_update=False):
    auto_update_flags[stop_id] = False
    if auto_update:
        button = tk.Button(root, text=text, command=lambda: start_auto_update(stop_id))
    else:
        button = tk.Button(root, text=text, command=lambda: start_fetching(stop_id))
    button.pack(side=tk.LEFT)

# Create buttons for specific stops with auto-update enabled
create_button('1106', 'Hennepin S', auto_update=True)
create_button('1321', 'Hennepin N', auto_update=True)
create_button('50212', 'Lake E', auto_update=True)
create_button('3523', 'Lagoon W', auto_update=True)

# Start the main event loop
root.mainloop()
