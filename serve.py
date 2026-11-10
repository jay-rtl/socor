"""Local static preview with clean URLs and the site's custom 404 page."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlsplit, unquote
import os

ROOT = Path(__file__).parent.resolve()
os.chdir(ROOT)

class Handler(SimpleHTTPRequestHandler):
    def send_head(self):
        route = unquote(urlsplit(self.path).path)
        candidate = (ROOT / route.lstrip('/')).resolve()
        if candidate.is_relative_to(ROOT) and candidate.is_dir() and (candidate / 'index.html').is_file():
            self.path = route.rstrip('/') + '/index.html'
        elif not candidate.is_relative_to(ROOT) or not candidate.is_file():
            data = (ROOT / '404.html').read_bytes()
            self.send_response(404)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            if self.command != 'HEAD':
                self.wfile.write(data)
            return None
        return super().send_head()

if __name__ == '__main__':
    print('SOCOR preview: http://localhost:3000', flush=True)
    ThreadingHTTPServer(('0.0.0.0', 3000), Handler).serve_forever()
