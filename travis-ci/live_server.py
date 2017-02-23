#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

PORT_NUMBER = 9876

class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/ok":
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.send_header('X-Custom-Header','header-test')
            self.end_headers()
            self.wfile.write("ok")
            return
        elif self.path == "/403":
            self.send_response(403)
            self.end_headers()
            self.wfile.write("Forbidden")
            return

        self.send_response(404)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write("Not Found")
        return


server = HTTPServer(('localhost', PORT_NUMBER), myHandler)
server.serve_forever()
