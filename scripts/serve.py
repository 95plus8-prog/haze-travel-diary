#!/usr/bin/env python3
"""Static file server that avoids os.getcwd()/os.path.abspath (both are
blocked by the sandbox this runs under). Directory is a hardcoded literal."""
import http.server
import socketserver

DIRECTORY = "/Volumes/Raid16/Claude/code/漫画作品展示网站"
PORT = 4173


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map, ".svg": "image/svg+xml", ".json": "application/json"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)


socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"serving {DIRECTORY} at port {PORT}")
    httpd.serve_forever()
