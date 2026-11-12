"""Create an offline dashboard. Pass the output filename as the first argument."""
from pathlib import Path
import json
import sys
from localization import script

here = Path(__file__).resolve().parent
city = here / "city"
read_json = lambda path: json.loads(path.read_text(encoding="utf-8"))
data = {
    "population": read_json(here / "population.json"),
    "systems": read_json(here / "systems.json"),
    "cities": {key: read_json(city / name) for key, name in (
        ("hk", "data.json"), ("approvals", "approvals.json"), ("plans", "plans.json"),
        ("gz", "guangzhou.json"))},
}
blocks = {"DATA": json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")}
for key, path in {
    "CITY_COHORT": city / "model.js", "CITY_HK": city / "network.js", "CITY_GZ": city / "guangzhou.js",
    "MODEL": here / "pipeline.js", "UI": here / "ui.js"
}.items():
    blocks[key] = path.read_text(encoding="utf-8")
blocks["LOCALIZE"] = script()
html = (here / "interface.html").read_text(encoding="utf-8")
for key, block in blocks.items():
    tag = f"/*{key}*/"
    assert html.count(tag) == 1
    html = html.replace(tag, block)
Path(sys.argv[1]).write_text(html, encoding="utf-8")
