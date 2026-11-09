"""Copy the installed Cupcake 0.1.4 viewer and schemas for a reproducible local demo."""
from pathlib import Path
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
EXTENSION = Path.home() / '.vscode/extensions/moh70-pawslab-pitt.cupcake-vscode-0.1.4'

def main():
    if not EXTENSION.exists():
        raise SystemExit(f'Install Cupcake Activity Authoring 0.1.4 first: {EXTENSION}')
    destination = ROOT / 'web/vendor/cupcake'
    shutil.copytree(EXTENSION / 'resources/viewer', destination, dirs_exist_ok=True)
    shutil.copytree(EXTENSION / 'schemas', ROOT / 'schemas', dirs_exist_ok=True)
    shutil.copytree(EXTENSION / 'resources/tutorials', ROOT / 'research/extension-tutorials', dirs_exist_ok=True)
    shutil.copy2(EXTENSION / 'README.md', ROOT / 'research/extension-README.md')
    manifest = {
        'name': 'Cupcake Activity Authoring for VS Code',
        'version': '0.1.4', 'publisher': 'moh70-pawslab-pitt',
        'license_declared_by_extension': 'MIT',
        'source': str(EXTENSION),
        'note': 'Unmodified local viewer bundle. No upstream license file was included in this installation. Preserve provenance; confirm notices before public redistribution.',
        'files': {str(p.relative_to(destination)): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in sorted(destination.rglob('*')) if p.is_file()}
    }
    (destination / 'PROVENANCE.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print(f'Copied {len(manifest["files"])} viewer assets and official schemas.')

if __name__ == '__main__':
    main()
