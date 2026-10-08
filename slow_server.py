import time
from http.server import BaseHTTPRequestHandler as handles
from http.server import HTTPServer as the_doctor

class SlowHandler(handles):
    def do_GET(self):
        time.sleep(10)
        
slow_server = the_doctor(('localhost',8081), SlowHandler)

slow_server.serve_forever()