"""Install a pinned, workspace-local WinLibs GCC toolchain; leave system PATH unchanged."""
from pathlib import Path
import hashlib
import json
import urllib.request
import zipfile

ROOT=Path(__file__).resolve().parents[1]
TAG='16.2.0posix-23.1.3-14.0.0-ucrt-r3'
ASSET='winlibs-x86_64-posix-seh-gcc-16.2.0-mingw-w64ucrt-14.0.0-r3.zip'
directory=ROOT/'.tools/gcc'
directory.mkdir(parents=True,exist_ok=True)
metadata=json.load(urllib.request.urlopen('https://api.github.com/repos/brechtsanders/winlibs_mingw/releases/tags/'+TAG))
asset=next(a for a in metadata['assets'] if a['name']==ASSET)
archive=ROOT/'.tools'/ASSET
if not archive.exists() or archive.stat().st_size!=asset['size']:
    print('Downloading workspace-local GCC 16.2.0...',flush=True)
    urllib.request.urlretrieve(asset['browser_download_url'],archive)
digest=hashlib.sha256(archive.read_bytes()).hexdigest()
expected=asset.get('digest')
if expected and expected!='sha256:'+digest:raise SystemExit('Toolchain checksum mismatch.')
if not (directory/'mingw64/bin/g++.exe').exists():
    print('Extracting the portable compiler...',flush=True)
    with zipfile.ZipFile(archive) as z:
        for member in z.infolist():
            target=(directory/member.filename).resolve()
            if not target.is_relative_to(directory.resolve()):raise SystemExit('Unsafe archive path.')
        z.extractall(directory)
provenance=dict(release=metadata['html_url'],asset=ASSET,url=asset['browser_download_url'],sha256=digest,
                publisherDigest=expected,compiler='16.2.0',standard='c++23')
(ROOT/'research/compiler-provenance.json').write_text(json.dumps(provenance,indent=2),encoding='utf-8')
print('Ready:',directory/'mingw64/bin/g++.exe',flush=True)
