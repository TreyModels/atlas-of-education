from pathlib import Path
import json
import sys

here = Path(__file__).resolve().parent
sys.path.insert(0, str(here.parent))
from localization import script
html = (here / "interface.html").read_text()
data = {name: json.loads((here / path).read_text()) for name,path in [
    ("hk","data.json"),("profiles","primary-profiles.json"),("approvals","approvals.json"),
    ("plans","plans.json"),("gz","guangzhou.json")
]}
blocks = {"DATA":json.dumps(data,ensure_ascii=False,separators=(",",":")).replace("<","\\u003c")}
for marker,path in [("STYLE","style.css"),("COHORT","model.js"),("HK","network.js"),("GZ","guangzhou.js"),("UI","ui.js")]:
    blocks[marker] = (here / path).read_text()
blocks["LOCALIZE"] = script()
for marker, content in blocks.items():
    tag = f"/*{marker}*/"
    assert html.count(tag) == 1
    html = html.replace(tag,content)
Path(sys.argv[1]).write_text(html,encoding="utf-8")
