import http.server as hts
import platform as pl
import psutil as ps
import time as t
import json

SERVER_IP = "192.168.1.216" # Your local IP
SERVER_PORT = 2005 # Default port is 2005
REPORT_TEMPS = True # This can be disabled if the OS doesn't support temperatures or errors out when getting the temperature.
REPORT_FANS = True # Same thing here

class Server(hts.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        
        data_to_send = { # This dictionary will be sent to the server. If you want to add custom metrics, start here.
            "cpu_percent": ps.cpu_percent(),
            "cpu_times_user": ps.cpu_times_percent().user,
            "cpu_times_system": ps.cpu_times_percent().system,
            "cpu_times_idle": ps.cpu_times_percent().idle,
            "cpu_freq_max": ps.cpu_freq().max,
            "cpu_freq_current": ps.cpu_freq().current,
            "cpu_freq_min": ps.cpu_freq().min,
            "mem_total": ps.virtual_memory().total,
            "mem_available": ps.virtual_memory().available,
            "mem_percent": ps.virtual_memory().percent,
            "disk_total": ps.disk_usage("/").total,
            "disk_used": ps.disk_usage("/").used,
            "disk_free": ps.disk_usage("/").free,
            "disk_percent": ps.disk_usage("/").percent,
            "temperature": ps.sensors_temperatures(True)["cpu_thermal"][0].current if REPORT_TEMPS else -99999, # This returns the first CPU temperature sensor's value in Fahrenheit. Change if you want it to send a different sensor's value.
            "name": pl.node()
        }
        
        def output(jsondt):
            self.wfile.write(bytes(json.dumps(jsondt), encoding="utf-8"))
        output(data_to_send)

server = hts.HTTPServer((SERVER_IP, SERVER_PORT), Server)
print(f"Server is online at port {SERVER_PORT}")
server.serve_forever()