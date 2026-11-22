"""Dev server: serves this folder and proxies /api/* to the FastAPI backend.

The backend has no CORS configuration, so proxying keeps the browser on one origin.
Usage: python3 server.py [port]   (env BACKEND_URL, default http://localhost:8000)
"""
import os
import sys
import urllib.error
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

BACKEND = os.environ.get("BACKEND_URL", "http://localhost:8000").rstrip("/")


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=os.path.dirname(os.path.abspath(__file__)), **kw)

    def do_GET(self):
        if self.path.startswith("/api/"):
            return self.proxy()
        super().do_GET()

    def proxy(self):
        try:
            with urllib.request.urlopen(BACKEND + self.path, timeout=10) as r:
                body, status, ctype = r.read(), r.status, r.headers.get("Content-Type")
        except urllib.error.HTTPError as e:
            body, status, ctype = e.read(), e.code, e.headers.get("Content-Type")
        except Exception as e:
            body, status, ctype = f'{{"detail":"Backend unreachable: {e}"}}'.encode(), 502, "application/json"
        self.send_response(status)
        self.send_header("Content-Type", ctype or "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5500
    print(f"Frontend on http://localhost:{port}  ->  backend {BACKEND}")
    ThreadingHTTPServer(("", port), Handler).serve_forever()
