from wsgiref.simple_server import make_server
import json
libros = []
contador_id = 1

def app(environ, start_response):
    global contador_id
    path = environ["PATH_INFO"]
    metodo = environ["REQUEST_METHOD"]

    if path == "/libros" and metodo == "GET":
        start_response("200 OK", [("Content-Type", "application/json")])
        return [json.dumps(libros).encode()]

    elif path == "/libros" and metodo == "POST":
        length = int(environ.get("CONTENT_LENGTH", 0))
        body = environ["wsgi.input"].read(length)
        data = json.loads(body)

        nuevo = {
            "id": contador_id,
            "titulo": data["titulo"],
            "autor": data["autor"],
            "anio": data["anio"]
        }
        libros.append(nuevo)
        contador_id += 1

        start_response("200 OK", [("Content-Type", "application/json")])
        return [json.dumps(nuevo).encode()]

    elif path.startswith("/libros/") and metodo == "GET":
        try:
            libro_id = int(path.split("/")[-1])
            libro = next(l for l in libros if l["id"] == libro_id)
            start_response("200 OK", [("Content-Type", "application/json")])
            return [json.dumps(libro).encode()]
        except:
            start_response("404 Not Found", [("Content-Type", "text/plain")])
            return [b"Libro no encontrado"]

    start_response("404 Not Found", [("Content-Type", "text/plain")])
    return [b"Ruta no encontrada"]

server = make_server("localhost", 8000, app)
print("Servidor WSGI corriendo en http://localhost:8000")
server.serve_forever()
