"""Local deck preview with atomic, conflict-aware JSON persistence.
Run: python3 server.py --port 8793
"""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlsplit
import argparse
import hashlib
import json
import os
import tempfile
import threading

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / 'deck-content.json'
LOCK = threading.Lock()

def load_document():
    document = json.loads(CONTENT.read_text(encoding='utf-8'))
    if document.get('schemaVersion') != 1 or not isinstance(document.get('texts'), dict):
        raise ValueError('deck-content.json 格式无效')
    if not all(isinstance(k, str) and isinstance(v, str) for k, v in document['texts'].items()):
        raise ValueError('texts 必须为文字键值表')
    revision = hashlib.sha256(json.dumps(document, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    return {**document, 'revision': revision}

def write_document(document):
    data = {k: v for k, v in document.items() if k != 'revision'}
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=ROOT, prefix='.deck-', suffix='.tmp', delete=False) as stream:
        temp_path = Path(stream.name)
        json.dump(data, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())
    try:
        os.replace(temp_path, CONTENT)
    finally:
        temp_path.unlink(missing_ok=True)

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def reply(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if urlsplit(self.path).path != '/api/content':
            return super().do_GET()
        try:
            with LOCK:
                self.reply(200, load_document())
        except (ValueError, OSError) as error:
            self.reply(422, {'error': str(error)})

    def do_POST(self):
        if urlsplit(self.path).path != '/api/content':
            return self.reply(404, {'error': 'Not found'})
        origin = self.headers.get('Origin')
        if origin and urlsplit(origin).netloc != self.headers.get('Host'):
            return self.reply(403, {'error': 'Same-origin requests only'})
        if self.headers.get('Content-Type', '').split(';')[0] != 'application/json':
            return self.reply(415, {'error': 'Expected JSON'})
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 1000000:
                return self.reply(413, {'error': 'Invalid payload size'})
            payload = json.loads(self.rfile.read(length))
            changes = payload.get('changes')
            if not isinstance(changes, dict) or len(changes) > 300:
                raise ValueError('Invalid changes')
            for key, change in changes.items():
                if not isinstance(key, str) or not isinstance(change, dict) or not isinstance(change.get('after'), str) or len(change['after']) > 20000:
                    raise ValueError('Invalid text change')
            with LOCK:
                document = load_document()
                texts = document['texts']
                conflicts = [key for key, change in changes.items() if texts.get(key) != change.get('before') and texts.get(key) != change['after']]
                if conflicts:
                    return self.reply(409, {'document': document, 'conflicts': conflicts})
                for key, change in changes.items():
                    texts[key] = change['after']
                if changes:
                    write_document(document)
                self.reply(200, load_document())
        except (ValueError, OSError, TypeError) as error:
            self.reply(422, {'error': str(error)})

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8793)
    args = parser.parse_args()
    server = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    print(f'Agent Deck Studio: http://127.0.0.1:{args.port}', flush=True)
    server.serve_forever()
