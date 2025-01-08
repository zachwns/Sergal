import tkinter as tk
from tkinter import ttk
import asyncio
import httpx
from plyer import notification
import threading

auto_update_flags = {}

async def fetch_data(stop_id):
    async with httpx.AsyncClient() as client:
        url = f'https://svc.metrotransit.org/nextrip/{stop_id}'
        response = await client.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Failed to retrieve data for stop_id {stop_id}:', response.status_code)
            return []

def update_ui(data, stop_id):
    print(f"Updating UI with fetched data for stop_id {stop_id}")
    tree.delete(*tree.get_children())
    if isinstance(data, list):
        for item in data:
            departure_text = item.get('departure_text', 'N/A')
            route_id = item.get('route_id', 'N/A')
            direction = item.get('direction_text', 'N/A')
            tree.insert('', 'end', text=route_id, values=(departure_text, direction))
            if departure_text == '5 Min':
                show_notification(route_id, direction, departure_text)

def show_notification(route_id, direction, departure_text):
    title = "Metro Transit Notification"
    message = f"Route {route_id} is due in {departure_text}"
    threading.Thread(target=lambda: notification.notify(
        title=title,
        message=message,
        timeout=5
    )).start()

def start_fetching(stop_id):
    def fetch_and_update():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        print(f"Starting fetch for {stop_id}")
        data = loop.run_until_complete(fetch_data(stop_id))
        update_ui(data.get('departures', []), stop_id)
        if auto_update_flags.get(stop_id, False):
            print(f"Scheduling next fetch for {stop_id}")
            root.after(30000, lambda: start_fetching(stop_id))
    
    threading.Thread(target=fetch_and_update).start()

def on_item_click(event):
    item_id = tree.selection()[0]
    item = tree.item(item_id)
    show_details(item['text'], item['values'])

def show_details(route_id, details):
    detail_window = tk.Toplevel(root)
    detail_window.title(f"Details for Route {route_id}")

    tk.Label(detail_window, text=f"Route ID: {route_id}").pack()
    tk.Label(detail_window, text=f"Due Time: {details[0]}").pack()
    tk.Label(detail_window, text=f"Direction: {details[1]}").pack()
    tk.Label(detail_window, text="Additional info here...").pack()

    tk.Button(detail_window, text="Close", command=detail_window.destroy).pack()

def start_auto_update(stop_id):
    auto_update_flags[stop_id] = True
    start_fetching(stop_id)

def stop_auto_update(stop_id):
    auto_update_flags[stop_id] = False

root = tk.Tk()
root.title('Metro Transit Data')

tree = ttk.Treeview(root)
tree['columns'] = ('departure_text', 'direction')
tree.column('#0', width=100, minwidth=100)
tree.column('departure_text', width=100, minwidth=100)
tree.column('direction', width=200, minwidth=200)

tree.heading('#0', text='Route ID', anchor=tk.W)
tree.heading('departure_text', text='Due Time', anchor=tk.W)
tree.heading('direction', text='Direction', anchor=tk.W)

tree.pack(side='top', fill='both', expand=True)

tree.bind('<Double-1>', on_item_click)

def create_button(stop_id, text, auto_update=False):
    auto_update_flags[stop_id] = False
    if auto_update:
        button = tk.Button(root, text=text, command=lambda: start_auto_update(stop_id))
    else:
        button = tk.Button(root, text=text, command=lambda: start_fetching(stop_id))
    button.pack(side=tk.LEFT)

create_button('1106', 'Hennepin S', auto_update=True)
create_button('1321', 'Hennepin N', auto_update=True)
create_button('50212', 'Lake E', auto_update=True)
create_button('3523', 'Lagoon W', auto_update=True)

root.mainloop()
