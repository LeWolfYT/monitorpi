import tkinter as tk
import tkinter.ttk as ttk
import requests as r
import threading as th
import time

POLL_INTERVAL = 1 # Poll interval in seconds
SERVER_IP = "192.168.1.219" # This is going to be the local IP of your server.
SERVER_PORT = 2005 # Default port is 2005

root = tk.Tk()
root.title("Server Monitor - Connecting...")
root.geometry("500x100")
available = True

def theloop():
    while available:
        time.sleep(POLL_INTERVAL)
        try:
            data_received = r.get(f"http://{SERVER_IP}:{SERVER_PORT}").json()
            root.title = f"Server Monitor - {data_received['name']} @ {SERVER_IP}"
        except:
            pass

lt = th.Thread(target=theloop)
lt.start()

root.mainloop()
available = False