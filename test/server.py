import os
import ssl
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from functools import partial


class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        if not os.environ.get("TEST_SERVER_NO_COOP"):
            self.send_header("Cross-Origin-Opener-Policy", "same-origin")
            self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        super().end_headers()


server = ThreadingHTTPServer(
    ("localhost", int(os.environ.get("TEST_SERVER_PORT", 8000))),
    partial(MyHTTPRequestHandler, directory="dist"),
)

if os.environ.get("TEST_SERVER_HTTPS"):
    server.socket = ssl.wrap_socket(
        server.socket,
        server_side=True,
        certfile="server.pem",
        ssl_version=ssl.PROTOCOL_TLS,
    )

server.serve_forever()
