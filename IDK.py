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

print (fetch_data)