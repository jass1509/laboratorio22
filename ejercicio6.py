from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class SumaHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers["Content-Length"])
        body = self.rfile.read(length)
        data = json.loads(body)

        resultado = {"suma": data.get("a", 0) + data.get("b", 0)}
        print(resultado)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(resultado).encode())

server = HTTPServer(("localhost", 8000), SumaHandler)
print("Servidor corriendo en http://localhost:8000")
server.serve_forever()
