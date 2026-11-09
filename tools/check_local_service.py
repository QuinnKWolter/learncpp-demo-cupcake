"""Exercise local HTTP execution/guidance integration, without browser automation."""
import json
import os
from pathlib import Path
import re
from urllib.request import Request,urlopen
from urllib.error import HTTPError

ROOT=Path(__file__).resolve().parents[1]
BASE=os.environ.get('CUPCAKE_TEST_URL','http://127.0.0.1:5173').rstrip('/')
def read(path):
    with urlopen(BASE+path,timeout=15) as response:return response.read()
def get(path):return json.loads(read(path))
health=get('/api/health');assert health['standard']=='c++23' and health['activities']==142
page=read('/activity.html').decode()
token=re.search(r"window.LOCAL_RUN_TOKEN='([^']+)'",page).group(1)
def run(activity_id,answers,origin=BASE):
    request=Request(BASE+'/api/run',data=json.dumps(dict(id=activity_id,answers=answers)).encode(),
                    headers={'Content-Type':'application/json','Origin':origin,'X-Cupcake-Local':token},method='POST')
    with urlopen(request,timeout=50) as response:return json.load(response)
checks=['Health reports C++23 revision 2 with 142 activities']
activity_id='cpp23-v2-02-functions-files-free-coding'
result=run(activity_id,['    return width * height;']);assert all(r['passed'] for r in result)
result=run(activity_id,['    return width + height;']);assert not all(r['passed'] for r in result)
checks.append('Live HTTP bridge executes correct code and rejects a plausible incorrect rule')
try:run(activity_id,['return 1;'],origin='https://unrelated.invalid');raise AssertionError('Foreign origin accepted')
except HTTPError as error:assert error.code==403
checks.append('Live HTTP bridge rejects a foreign Origin')
teaching=get('/api/teaching?id=cpp23-v2-02-functions-files-code-completion')
assert len(teaching['hints'])==2 and 'geometry.hpp' in teaching['supportingFiles']
activity=get('/api/activity?id=cpp23-v2-02-functions-files-code-completion')
assert 'distance around all four sides' in activity['statement']
assert 'rectanglePerimeter' in activity['includes']['geometry.hpp']
checks.append('Completion has its own goal, two hints, and the complete supporting header')
for path in ['/lib/jsvee/JSVEE-min.js','/lib/jsvee/jsvee.css','/activity-help.css','/lesson-markdown.js']:
    assert len(read(path))>100
checks.append('Macro runtime and guidance assets are served successfully')
bundle=read('/vendor/cupcake/chunk-VQLJXNIZ.js')
assert b'i.running||!i.isCodeChanged()' not in bundle
assert b'i.running||!i.isCodeChanged()' in (ROOT/'web/vendor/cupcake/chunk-VQLJXNIZ.js').read_bytes()
checks.append('Served recheck adjustment is active while the pinned vendor file stays intact')
report=dict(kind='live loopback HTTP integration checks',browserTest=False,passed=len(checks),checks=checks)
reports=Path(os.environ.get('CUPCAKE_REPORT_DIR', ROOT/'research'))
reports.mkdir(parents=True,exist_ok=True)
(reports/'service-checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
