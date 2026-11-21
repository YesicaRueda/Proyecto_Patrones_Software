"""Servidor local de la visual del MES (solo biblioteca estándar).

Uso (desde la raíz del proyecto):

    python -m src.gui.server            # abre http://127.0.0.1:8765 en el navegador
    python -m src.gui.server --port 9000 --no-browser
"""
import argparse
import json
import os
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs

from src.gui.controller import DashboardController

HTML = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard.html")


def make_handler(controller):
    class Handler(BaseHTTPRequestHandler):
        def _send(self, code, body, content_type="application/json; charset=utf-8"):
            data = body if isinstance(body, bytes) else json.dumps(body, ensure_ascii=False).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            path, _, query = self.path.partition("?")
            if path in ("/", "/index.html"):
                with open(HTML, "rb") as f:
                    self._send(200, f.read(), "text/html; charset=utf-8")
            elif path == "/api/state":
                try:
                    since = int(parse_qs(query).get("since", ["0"])[0])
                except ValueError:
                    since = 0
                self._send(200, controller.state(since))
            else:
                self._send(404, {"error": "No encontrado"})

        def do_POST(self):
            if self.path != "/api/action":
                self._send(404, {"error": "No encontrado"})
                return
            try:
                length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(length) or b"{}")
                action = payload.pop("action")
            except (ValueError, KeyError):
                self._send(400, {"ok": False, "error": "Solicitud inválida"})
                return
            self._send(200, controller.act(action, **payload))

        def log_message(self, *args):  # sin ruido en la consola
            pass

    return Handler


def main(argv=None):
    parser = argparse.ArgumentParser(description="Visual del MES (Observer en vivo)")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args(argv)

    controller = DashboardController()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(controller))
    url = f"http://127.0.0.1:{args.port}"
    print(f"Visual del MES en {url}  (Ctrl+C para cerrar)")
    if not args.no_browser:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nCerrado.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
