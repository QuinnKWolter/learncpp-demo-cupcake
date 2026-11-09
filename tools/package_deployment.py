"""Create a curated server handoff, excluding local tools, downloads and user data."""
from pathlib import Path
import hashlib
import json
import tarfile
from check_installation import main as check_installation

ROOT = Path(__file__).resolve().parents[1]
DIRECTORIES = ('content', 'course', 'schemas', 'web', 'tools', 'docs', 'deploy')
FILES = ('Dockerfile', 'docker-compose.yml', '.dockerignore', '.gitattributes', '.gitignore',
         'requirements.txt', 'requirements.lock', 'server.py', 'README.md', 'LICENSE')


def main():
    check_installation()
    paths = [ROOT / name for name in FILES]
    for name in DIRECTORIES:
        paths.extend(p for p in (ROOT / name).rglob('*') if p.is_file()
                     and '__pycache__' not in p.parts and p.suffix not in ('.pyc', '.log'))
    paths = sorted(paths)
    destination = ROOT / 'exports'
    destination.mkdir(exist_ok=True)
    archive = destination / 'cupcake-lab-deploy.tar.gz'
    # Explicit file list; no hidden runtime, Windows compiler, or research downloads.
    with tarfile.open(archive, 'w:gz', format=tarfile.PAX_FORMAT) as tar:
        for path in paths:
            info = tar.gettarinfo(str(path), 'cupcake-lab/' + path.relative_to(ROOT).as_posix())
            info.uid = info.gid = 0
            info.uname = info.gname = ''
            info.mode = 0o644
            with path.open('rb') as stream:
                tar.addfile(info, stream)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (destination / (archive.name + '.sha256')).write_text(f'{digest}  {archive.name}\n', encoding='ascii')
    report = dict(archive=archive.name, bytes=archive.stat().st_size, sha256=digest,
                  files={p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
    (destination / 'deployment-manifest.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(f'{archive}\n{archive.stat().st_size:,} bytes; {len(paths)} files\nSHA256 {digest}')


if __name__ == '__main__':
    main()
