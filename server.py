"""C++ course server for trusted users; see docs/DEPLOYMENT.md for Docker/SSH hosting."""
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlsplit, parse_qs, unquote
import argparse
import json
import mimetypes
import os
import secrets
import sys
import threading
import yaml

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools'))
from execution import execute,COMPILER,STANDARD

TOKEN=secrets.token_urlsafe(32)
RUN_LOCK=threading.Lock()
MANIFEST=json.loads((ROOT/'web/course.json').read_text(encoding='utf-8'))
ACTIVITIES={a['id']:a for a in MANIFEST['modules'] for a in a['activities']}
ACTIVITIES.update({a['id']:a for a in MANIFEST['capstones']})

def get_activity(activity_id):
    entry=ACTIVITIES.get(activity_id)
    if not entry:raise ValueError('Unknown activity id.')
    return yaml.safe_load((ROOT/entry['path']).read_text(encoding='utf-8'))

class Handler(BaseHTTPRequestHandler):
    server_version='CupcakeLocal/1.0'
    def setup(self):
        super().setup()
        self.connection.settimeout(15)
    def origin(self):return f'http://{self.headers.get("Host","")}'
    def trusted_host(self):
        return self.headers.get('Host') in (f'127.0.0.1:{self.server.server_port}',f'localhost:{self.server.server_port}')
    def reply(self,status,body,content_type='application/json; charset=utf-8'):
        data=body if isinstance(body,bytes) else json.dumps(body,ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header('Content-Type',content_type)
        self.send_header('Content-Length',str(len(data)))
        self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Referrer-Policy','strict-origin-when-cross-origin')
        # Embedding is intentional. Source/origin checks in the host bind messages to its iframe.
        self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:; connect-src 'self'; frame-src 'self'; base-uri 'self'; object-src 'none'")
        self.end_headers();self.wfile.write(data)
    def do_GET(self):
        if not self.trusted_host():return self.reply(403,{'error':'Loopback host required.'})
        url=urlsplit(self.path);path=unquote(url.path)
        if path=='/api/health':return self.reply(200 if COMPILER else 503,dict(ok=bool(COMPILER),compiler=bool(COMPILER),standard=STANDARD,revision=MANIFEST.get('revision'),activities=len(ACTIVITIES)))
        if path=='/api/teaching':
            entry=ACTIVITIES.get(parse_qs(url.query).get('id',[''])[0])
            if not entry:return self.reply(404,dict(error='Unknown activity.'))
            return self.reply(200,entry.get('guide',{}))
        if path=='/api/activity':
            try:return self.reply(200,get_activity(parse_qs(url.query).get('id',[''])[0]))
            except ValueError as e:return self.reply(404,dict(error=str(e)))
        if path.startswith('/lib/'):
            base=ROOT/'web/vendor/cupcake/lib';candidate=(base/path.removeprefix('/lib/')).resolve()
        elif path.startswith('/content/'):
            base=ROOT/'course';candidate=(ROOT/path.removeprefix('/content/')).resolve()
        elif path.startswith('/schemas/'):
            base=ROOT/'schemas';candidate=(ROOT/path.lstrip('/')).resolve()
        else:
            base=ROOT/'web';candidate=(base/('index.html' if path=='/' else path.lstrip('/'))).resolve()
        if not candidate.is_relative_to(base.resolve()) or not candidate.is_file():return self.reply(404,dict(error='Not found.'))
        data=candidate.read_bytes()
        if candidate.name=='chunk-VQLJXNIZ.js':
            # Version-pinned compatibility fix: let restored or unchanged code be checked.
            # Keep the vendor file intact; only the served response changes. Compilation
            # still validates blank/incomplete work and no grade is manufactured here.
            old=b'i.running||!i.isCodeChanged()'
            if data.count(old)!=1:return self.reply(500,dict(error='Viewer compatibility patch needs review.'))
            data=data.replace(old,b'i.running')
        if candidate==ROOT/'web/activity.html':data=data.replace(b'__LOCAL_RUN_TOKEN__',TOKEN.encode())
        kind=mimetypes.guess_type(candidate.name)[0] or 'application/octet-stream'
        if candidate.suffix=='.js':kind='text/javascript'
        if candidate.suffix=='.yaml':kind='text/yaml'
        self.reply(200,data,kind+('; charset=utf-8' if kind.startswith('text/') else ''))
    def do_POST(self):
        if not self.trusted_host() or self.headers.get('Origin')!=self.origin() or self.headers.get('X-Cupcake-Local')!=TOKEN:
            return self.reply(403,dict(error='Same-origin local execution token required.'))
        if urlsplit(self.path).path!='/api/run':return self.reply(404,dict(error='Not found.'))
        try:
            length=int(self.headers.get('Content-Length','0'))
            if length<=0 or length>150000:raise ValueError('Request size out of range.')
            payload=json.loads(self.rfile.read(length))
            if not isinstance(payload,dict):raise ValueError('Expected a JSON object.')
            task=get_activity(payload.get('id',''))
            for field in ['answers','selections']:
                if field in payload and (not isinstance(payload[field],list) or len(payload[field])>40):raise ValueError('Invalid '+field)
            if not RUN_LOCK.acquire(blocking=False):return self.reply(429,dict(error='Another compilation is still running.'))
            try:result=execute(task,payload)
            finally:RUN_LOCK.release()
            return self.reply(200,result)
        except (ValueError,KeyError,TypeError,IndexError) as e:return self.reply(400,dict(error=str(e)))
        except Exception as e:return self.reply(500,dict(error=str(e)))
    def log_message(self,format,*args):
        # Log routes and HTTP status only, never code answers, tokens, or learner events.
        print(format % args,flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--port',type=int,default=5173)
    parser.add_argument('--host',choices=['127.0.0.1','0.0.0.0'],default=os.environ.get('CUPCAKE_BIND_HOST','127.0.0.1'),help='Use 0.0.0.0 only inside the loopback-published Docker deployment.')
    args=parser.parse_args()
    httpd=ThreadingHTTPServer((args.host,args.port),Handler)
    print(f'C++ Studio listening on {args.host}:{args.port}\n{len(ACTIVITIES)} Cupcake activities. Compiler: {COMPILER}\nTrusted users only; access via localhost or SSH tunnel. Ctrl+C to stop.',flush=True)
    try:httpd.serve_forever()
    except KeyboardInterrupt:pass
    finally:httpd.server_close()
