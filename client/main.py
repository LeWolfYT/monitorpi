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
root.geometry("500x175")
available = True
connected = False

# Get rid of the default window menu (especially on macOS)
menu = tk.Menu(root)
root.config(menu=menu)

# Setting up labels
cpupl = ttk.Label(root, text="CPU Usage: Loading...")
cpupl.place(x=5, y=5)
cpup = ttk.Progressbar(root, mode="determinate", value=0)
cpup.place(x=5, y=25, relwidth=1, width=-10)
mempl = ttk.Label(root, text="RAM Usage: Loading...")
mempl.place(x=5, y=45)
memp = ttk.Progressbar(root, mode="determinate", value=0)
memp.place(x=5, y=65, relwidth=1, width=-10)
diskpl = ttk.Label(root, text="Disk Usage: Loading...")
diskpl.place(x=5, y=85)
diskp = ttk.Progressbar(root, mode="determinate", value=0)
diskp.place(x=5, y=105, relwidth=1, width=-10)
temppl = ttk.Label(root, text="Temperature: Loading...")
temppl.place(x=5, y=125)
tempp = ttk.Progressbar(root, mode="determinate", value=0, maximum=212)
tempp.place(x=5, y=145, relwidth=1, width=-10)

def theloop():
    while available:
        try:
            data_received = r.get(f"http://{SERVER_IP}:{SERVER_PORT}").json() # Get the stats from the server
            # Tons of setting labels to reflect the new data
            root.title(f"Server Monitor - {data_received['name']} @ {SERVER_IP}")
            cpupl.config(text=f"CPU Usage: {data_received['cpu_percent']}% - Running @{round(data_received['cpu_freq_current'])}MHz {'(minimum)' if data_received['cpu_freq_current']==data_received['cpu_freq_min'] else ''}{'(maximum)' if data_received['cpu_freq_current']==data_received['cpu_freq_max'] else ''}")
            cpup.config(value=data_received["cpu_percent"])
            mempl.config(text=f"RAM Usage: {data_received['mem_percent']}% ({round((data_received['mem_total'] - data_received['mem_available'])/1024/1024)}MiB / {round(data_received['mem_total']/1024/1024)}MiB Total)")
            memp.config(value=data_received["mem_percent"])
            diskpl.config(text=f"Disk Usage: {data_received['disk_percent']}% ({round(data_received['disk_used']/1024/1024/1024)}GiB / {round(data_received['disk_total']/1024/1024/1024)}GiB Total)")
            diskp.config(value=data_received["disk_percent"])
            temppl.config(text=f"Temperature: {round(data_received['temperature'], 1)}°F")
            tempp.config(value=data_received["temperature"])
            connected = True
        except r.ConnectionError:
            # This is what happens if it is disconnected.
            if connected:
                root.title("Server Monitor - Attempting to reconnect...")
                cpupl.config(text=f"CPU Usage: Loading...")
                cpup.config(value=0)
                mempl.config(text=f"RAM Usage: Loading...")
                memp.config(value=0)
                diskpl.config(text=f"Disk Usage: Loading...")
                diskp.config(value=0)
                temppl.config(text=f"Temperature: Loading...")
                tempp.config(value=0)
        except:
            pass
        for i in range(POLL_INTERVAL*5):
            time.sleep(0.2)
            if not available:
                break

lt = th.Thread(target=theloop)
lt.start()

root.mainloop()
available = False