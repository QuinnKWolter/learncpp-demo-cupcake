"""Dependency-free container health probe; no compilation per probe."""
import json
from urllib.request import urlopen

with urlopen('http://127.0.0.1:5173/api/health', timeout=3) as response:
    health = json.load(response)
if not (health.get('ok') and health.get('compiler') and health.get('standard') == 'c++23'
        and health.get('activities') == 142):
    raise SystemExit('Unexpected health response: ' + repr(health))
