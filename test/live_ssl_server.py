# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

try:
    from http.server import BaseHTTPRequestHandler, HTTPServer
except ImportError:
    from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import os
import ssl
import socketserver

PORT_NUMBER = 9443


class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/ok":
            cert = self.request.getpeercert()
            subject = b""
            if cert:
                subject = cert["subjectAltName"][0][1].encode("ascii")
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.send_header('X-Custom-Header','header-test')
            self.end_headers()
            self.wfile.write(b"ok: " + subject)
            return
        elif self.path == "/403":
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b"Forbidden")
            return

        self.send_response(404)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(b"Not Found")
        return


cert_path = os.path.join(os.path.dirname(__file__), 'certs/server-cert.pem')
key_path = os.path.join(os.path.dirname(__file__), 'certs/server_key.pem')
ca_path = os.path.join(os.path.dirname(__file__), 'certs/cacert.pem')

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_verify_locations(cafile=ca_path)
context.load_cert_chain(certfile=cert_path, keyfile=key_path)

with socketserver.TCPServer(('localhost', PORT_NUMBER), myHandler) as httpd:
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    httpd.serve_forever()
