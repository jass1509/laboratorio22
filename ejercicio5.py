from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>Hola</h1>")
        elif self.path == "/saludo":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"msg": "Hola"}).encode())
        else:
            self.send_response(404)
            self.end_headers()

server = HTTPServer(("localhost", 8000), Handler)
server.serve_forever()
