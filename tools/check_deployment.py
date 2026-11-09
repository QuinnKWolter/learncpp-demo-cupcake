"""Check the hosting adapter's subpath URLs, proxy origins and HEAD behavior.

These are HTTP deployment tests, separate from the unchanged 142-activity suite.
"""
import json
import re
import threading
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from serve_deployment import BASE_PATH, PUBLIC_ORIGIN, DeploymentHandler, server


def main():
    httpd = server.ThreadingHTTPServer(('127.0.0.1', 0), DeploymentHandler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    origin = f'http://127.0.0.1:{httpd.server_port}'

    def read(path, headers=None, data=None, method=None):
        request = Request(origin + path, headers=headers or {}, data=data, method=method)
        with urlopen(request, timeout=50) as response:
            return response.status, response.headers, response.read()

    def rejected(path, headers, data, expected):
        try:
            read(path, headers, data)
        except HTTPError as error:
            assert error.code == expected, error
        else:
            raise AssertionError('Request unexpectedly accepted: ' + path)

    try:
        # Both prefix-preserving and prefix-stripping upstream mappings work.
        for root in ('/', BASE_PATH + '/'):
            status, headers, body = read(root)
            assert status == 200
            assert f'src="{BASE_PATH}/studio.js"'.encode() in body
            assert f'href="{BASE_PATH}/studio.css"'.encode() in body
            assert b'src="/studio.js"' not in body
            status, head, empty = read(root, method='HEAD')
            assert status == 200 and not empty and int(head['Content-Length']) == len(body)
        _, _, html = read(BASE_PATH + '/activity.html')
        assert f'<base href="{BASE_PATH}/vendor/cupcake/">'.encode() in html
        token = re.search(rb"window.LOCAL_RUN_TOKEN='([^']+)'", html)[1].decode()
        assets = [BASE_PATH + '/' + path for path in (
            'studio.js', 'studio.css', 'activity.js', 'activity-help.css', 'lesson-markdown.js',
            'favicon.svg', 'course.json', 'vendor/cupcake/main.js', 'vendor/cupcake/styles.css',
            'lib/jsvee/JSVEE-min.js', 'lib/jsvee/jsvee.css')]
        for path in assets:
            assert read(path)[0] == 200, path
        studio = read(BASE_PATH + '/studio.js')[2]
        assert f"fetch('{BASE_PATH}/course.json')".encode() in studio
        assert ('${location.origin}' + BASE_PATH + '/activity.html').encode() in studio
        assert f'`{BASE_PATH}/?module='.encode() in studio
        activity = read(BASE_PATH + '/activity.js')[2]
        assert f"originalFetch('{BASE_PATH}/api/run'".encode() in activity
        assert b"endsWith('/api/v1/log')" in activity  # Keep telemetry suppression intact.
        loader = read(BASE_PATH + '/vendor/cupcake/chunk-PE6JJOUT.js')[2]
        assert f'"{BASE_PATH}/lib/jsvee/'.encode() in loader
        assert b'"/lib/jsvee/' not in loader
        manifest = json.loads(read(BASE_PATH + '/course.json')[2])
        entry = manifest['modules'][0]['activities'][0]
        assert read(BASE_PATH + '/content/' + entry['path'])[0] == 200
        assert json.loads(read(BASE_PATH + '/api/health')[2])['activities'] == 142
        payload = json.dumps(dict(id='cpp23-v2-02-functions-files-free-coding',
                                  answers=['    return width * height;'])).encode()
        for path, host in [(BASE_PATH + '/api/run', PUBLIC_ORIGIN.split('://')[1]),
                           ('/api/run', f'127.0.0.1:{httpd.server_port}')]:
            headers = {'Host': host, 'Origin': PUBLIC_ORIGIN, 'X-Cupcake-Local': token,
                       'Content-Type': 'application/json'}
            result = json.loads(read(path, headers, payload)[2])
            assert all(case['passed'] for case in result), result
        rejected(BASE_PATH + '/api/run', {'Origin': 'https://unrelated.invalid',
                 'X-Forwarded-Host': PUBLIC_ORIGIN.split('://')[1], 'X-Cupcake-Local': token}, payload, 403)
        rejected(BASE_PATH + '/api/run', {'Origin': PUBLIC_ORIGIN}, payload, 403)
        rejected(BASE_PATH + '/', {'Host': 'unrelated.invalid'}, None, 403)
        print('Deployment checks passed: subpath assets, APIs, iframe/export URLs, JSVEE, HEAD, '
              'preserved/rewritten proxy Host, and origin/token rejection.')
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join()


if __name__ == '__main__':
    main()
