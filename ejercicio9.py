from wsgiref.simple_server import make_server
import json, os, mimetypes
from urllib.parse import unquote

equipos = []
contador_id = 1
STATIC_DIR = "static"

def servir_estatico(path):
    file_path = path.lstrip("/")
    full_path = os.path.join(STATIC_DIR, file_path.replace("static/", ""))

    if not os.path.isfile(full_path):
        return None, None

    content_type, _ = mimetypes.guess_type(full_path)
    if content_type is None:
        content_type = "application/octet-stream"

    with open(full_path, "rb") as f:
        return f.read(), content_type

def app(environ, start_response):
    global contador_id
    metodo = environ["REQUEST_METHOD"]
    path = unquote(environ["PATH_INFO"])

    # Archivos estáticos
    if path.startswith("/static/"):
        contenido, tipo = servir_estatico(path)
        if contenido is None:
            start_response("404 Not Found", [("Content-Type", "text/plain")])
            return [b"Archivo no encontrado"]
        start_response("200 OK", [("Content-Type", tipo)])
        return [contenido]

    # API de equipos
    if path == "/equipos" and metodo == "GET":
        start_response("200 OK", [("Content-Type", "application/json")])
        return [json.dumps(equipos).encode()]

    elif path == "/equipos" and metodo == "POST":
        length = int(environ.get("CONTENT_LENGTH", 0))
        body = environ["wsgi.input"].read(length)
        data = json.loads(body)

        nuevo = {
            "id": contador_id,
            "nombre": data["nombre"],
            "ciudad": data["ciudad"],
            "nivelAtaque": data["nivelAtaque"],
            "nivelDefensa": data["nivelDefensa"]
        }
        equipos.append(nuevo)
        contador_id += 1

        start_response("200 OK", [("Content-Type", "application/json")])
        return [json.dumps(nuevo).encode()]

    elif path.startswith("/equipos/") and metodo == "GET":
        try:
            equipo_id = int(path.split("/")[-1])
            equipo = next(e for e in equipos if e["id"] == equipo_id)
            start_response("200 OK", [("Content-Type", "application/json")])
            return [json.dumps(equipo).encode()]
        except:
            start_response("404 Not Found", [("Content-Type", "text/plain")])
            return [b"Equipo no encontrado"]

    start_response("404 Not Found", [("Content-Type", "text/plain")])
    return [b"Ruta no encontrada"]

server = make_server("localhost", 8000, app)
print("Servidor WSGI avanzado corriendo en http://localhost:8000")
server.serve_forever()
