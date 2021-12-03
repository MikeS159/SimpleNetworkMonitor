import http.server
import socketserver
from urllib.parse import urlparse
from urllib.parse import parse_qs
import os
import requests

green = 0
red = 0

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.end_headers()
#        print (self.path)
        path = self.path
        ss = path.split('-')
#        print (ss)
        if(len(ss) == 2):
            if(ss[0] == '/ping'):
                #do ping
#                print ('ping ' + ss[1])
                response = os.system("ping -W 0.5 -c 1 " + ss[1])
                if(response == 0):
                    self.wfile.write(green)
                else:
                    self.wfile.write(red)
            if(ss[0] == '/load'):
                #do load
#                print ('load' + ss[1])
                try:
                    response = requests.get(ss[1], timeout=1)
                except:
                    self.wfile.write(red)
                    return
                if(response.status_code == 200):
                    self.wfile.write(green)
                else:
                    self.wfile.write(red)
        return

r = open('/path/to/red.png', 'rb')
g = open('/path/to/green.png', 'rb')
red = r.read()
green = g.read()

# Create an object of the above class
handler_object = MyHttpRequestHandler

PORT = 8000
try:
    my_server = socketserver.TCPServer(("", PORT), handler_object)
    print('Server started on port ' + str(PORT))
    # Star the server
    my_server.serve_forever()

except KeyboardInterrupt:
    print ('^C received, shutting down the web server')
    my_server.socket.close()
    r.close()
    g.close()
