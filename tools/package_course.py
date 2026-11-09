"""Export portable native activities; do not bundle runtime/user data or third-party viewer."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT=Path(__file__).resolve().parents[1]
destination=ROOT/'exports';destination.mkdir(exist_ok=True)
archive=destination/'cpp-course-cupcake.zip'
files=sorted((ROOT/'course/activities').rglob('*.yaml'))
manifest=json.loads((ROOT/'web/course.json').read_text(encoding='utf-8'))
count=manifest['activityCount']
files += [ROOT/'course/README.md',ROOT/'course/course.yaml',ROOT/'LICENSE',ROOT/'docs/AUTHORING.md',ROOT/'docs/SPLICE.md',ROOT/'docs/CXX23-REVIEW.md']
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for file in files:z.write(file,file.relative_to(ROOT).as_posix())
    z.writestr('PACKAGE-NOTES.txt',f'{count} native Cupcake activities for C++23. Each of 20 modules includes all seven activity types; two additional projects use free coding. course/course.yaml is a custom sequencing manifest, not an upstream Journey schema. Hosted execution must support C++23. Use existing Cupcake viewers or the local project host. LearnCpp readings are linked, not republished. No third-party viewer code or compiler is bundled in this archive.\n')
result=dict(file=str(archive),bytes=archive.stat().st_size,sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),activities=count,standard='C++23',revision=manifest['revision'])
(destination/'package.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
