"""Load the reviewed C++23 teaching sources used by the course builder."""
from pathlib import Path
import yaml

DIRECTORY=Path(__file__).resolve().parent
MODULES=[yaml.safe_load(p.read_text(encoding="utf-8")) for p in sorted((DIRECTORY/"modules").glob("*.yaml"))]
CAPSTONES=yaml.safe_load((DIRECTORY/"projects.yaml").read_text(encoding="utf-8"))
assert len(MODULES)==20, "Expected all twenty reviewed modules"
