"""Check the self-contained runtime and pinned third-party assets before shipping."""
from pathlib import Path
import hashlib
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]


def main():
    vendor = ROOT / 'web/vendor/cupcake'
    provenance = json.loads((vendor / 'PROVENANCE.json').read_text(encoding='utf-8'))
    for name, digest in provenance['files'].items():
        path = (vendor / Path(name.replace('\\', '/'))).resolve()
        if not path.is_relative_to(vendor.resolve()):
            raise ValueError('Invalid vendor path: ' + name)
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError('Vendor checksum mismatch: ' + name)
    patch = (vendor / 'chunk-VQLJXNIZ.js').read_bytes()
    if patch.count(b'i.running||!i.isCodeChanged()') != 1:
        raise ValueError('Viewer compatibility patch needs review.')
    manifest = json.loads((ROOT / 'web/course.json').read_text(encoding='utf-8'))
    entries = [a for m in manifest['modules'] for a in m['activities']] + manifest['capstones']
    if len(entries) != 142 or len({a['id'] for a in entries}) != 142:
        raise ValueError('Expected 142 distinct activities.')
    for entry in entries:
        path = (ROOT / entry['path']).resolve()
        if not path.is_relative_to((ROOT / 'course/activities').resolve()):
            raise ValueError('Invalid activity path.')
        task = yaml.safe_load(path.read_text(encoding='utf-8'))
        if task['id'] != entry['id']:
            raise ValueError('Manifest/activity mismatch: ' + entry['id'])
        if not (ROOT / 'schemas' / (task['pedagogy']['activity'] + '_0.1.0.json')).is_file():
            raise ValueError('Missing schema for ' + entry['id'])
    for name in ['index.html', 'activity.html', 'studio.js', 'studio.css', 'activity.js',
                 'activity-help.css', 'lesson-markdown.js']:
        if not (ROOT / 'web' / name).is_file():
            raise ValueError('Missing web asset: ' + name)
    print(f'Installation complete: {len(entries)} activities, {len(provenance["files"])} verified vendor assets.')


if __name__ == '__main__':
    main()
