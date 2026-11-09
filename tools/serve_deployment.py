"""Apache/subpath deployment adapter; keep validated server and web sources intact.

Only hosted asset responses are rebased. Course JSON/YAML and vendor files on disk
remain untouched. The original execution, grading and token checks are inherited.
"""
from io import BytesIO
from pathlib import Path
from urllib.parse import urlsplit
import os
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import server

BASE_PATH = os.environ.get('CUPCAKE_BASE_PATH', '/cupcake-lab').rstrip('/')
PUBLIC_ORIGIN = os.environ.get('CUPCAKE_PUBLIC_ORIGIN', 'https://adapt2.sis.pitt.edu')
public = urlsplit(PUBLIC_ORIGIN)
if not re.fullmatch(r'(?:/[A-Za-z0-9_-]+)+', BASE_PATH):
    raise ValueError('CUPCAKE_BASE_PATH must be a non-root path without a trailing slash.')
if (public.scheme not in ('http', 'https') or not public.netloc or public.path or
        public.query or public.fragment or public.username or public.password):
    raise ValueError('CUPCAKE_PUBLIC_ORIGIN must be an origin, without a path or trailing slash.')


def hosted_asset(path, data):
    """Rebase only known URL-bearing shell assets, never lesson/code payloads."""
    prefix = BASE_PATH.encode()
    if path in ('/', '/index.html', '/activity.html'):
        data = re.sub(rb'''((?:src|href)=["'])/(?!/)''', lambda m: m[1] + prefix + b'/', data)
        data = data.replace(b'This is a local learning demo; its native compiler runs as your user.',
                            b'C++ runs on the lab server for trusted collaborators.')
    elif path in ('/studio.js', '/activity.js'):
        data = re.sub(rb'''(["'`])/(?=(?:lesson-markdown\.js|\?module=|activity\.html|content/|course\.json|api/(?:run|activity|teaching)))''',
                      lambda m: m[1] + prefix + b'/', data)
        data = data.replace(b'${location.origin}/activity.html',
                            b'${location.origin}' + prefix + b'/activity.html')
        data = data.replace(b'The local server must be running on the viewing machine.',
                            b'The lab server must be available to the viewer.')
    elif path.startswith('/vendor/cupcake/') and path.endswith('.js'):
        # The upstream visualization loader creates root-relative script/style URLs.
        data = re.sub(rb'''(["'])/lib/''', lambda m: m[1] + prefix + b'/lib/', data)
    return data


class DeploymentHandler(server.Handler):
    def trusted_host(self):
        allowed = {public.netloc, f'127.0.0.1:{self.server.server_port}',
                   f'localhost:{self.server.server_port}', '127.0.0.1:20700', 'localhost:20700'}
        return self.headers.get('Host') in allowed

    def origin(self):
        # Support Apache with either preserved or rewritten Host. Do not trust
        # arbitrary Forwarded/X-Forwarded-* headers to choose a permitted origin.
        if self.headers.get('Host') == public.netloc or self.headers.get('Origin') == PUBLIC_ORIGIN:
            return PUBLIC_ORIGIN
        return super().origin()

    def normalize_path(self):
        # Apache can preserve /cupcake-lab/ or strip it from the upstream request.
        if self.path.startswith(BASE_PATH + '/'):
            self.path = self.path[len(BASE_PATH):]
        self.asset_path = urlsplit(self.path).path

    def reply(self, status, body, content_type='application/json; charset=utf-8'):
        if isinstance(body, bytes):
            body = hosted_asset(getattr(self, 'asset_path', ''), body)
        return super().reply(status, body, content_type)

    def do_GET(self):
        original = self.path
        if urlsplit(original).path == BASE_PATH:
            if not self.trusted_host():
                return self.reply(403, {'error': 'Configured host required.'})
            suffix = ('?' + urlsplit(original).query) if urlsplit(original).query else ''
            self.send_response(302)
            self.send_header('Location', BASE_PATH + '/' + suffix)
            self.send_header('Content-Length', '0')
            self.end_headers()
            return
        self.normalize_path()
        try:
            return super().do_GET()
        finally:
            self.path = original

    def do_POST(self):
        original = self.path
        self.normalize_path()
        try:
            return super().do_POST()
        finally:
            self.path = original

    def do_HEAD(self):
        # Reuse GET's status/headers (including compatibility transforms and length),
        # but send no body. This also supports the administrator's curl -I probe.
        output = self.wfile
        capture = BytesIO()
        self.wfile = capture
        try:
            self.do_GET()
        finally:
            self.wfile = output
        output.write(capture.getvalue().split(b'\r\n\r\n', 1)[0] + b'\r\n\r\n')


if __name__ == '__main__':
    httpd = server.ThreadingHTTPServer(('0.0.0.0', 5173), DeploymentHandler)
    print(f'C++ Studio: {PUBLIC_ORIGIN}{BASE_PATH}/; listening on container port 5173', flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
