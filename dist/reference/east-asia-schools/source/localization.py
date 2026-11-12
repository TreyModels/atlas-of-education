from pathlib import Path
import json

root = Path(__file__).resolve().parent

def script():
    labels = {}
    for line in (root / "locales.tsv").read_text(encoding="utf-8").splitlines():
        if line:
            key, chinese, vietnamese = line.split("\t")
            labels[key] = [chinese, vietnamese]
    content = (root / "localize.js").read_text(encoding="utf-8")
    return content.replace("/*LOCALES*/", json.dumps(labels, ensure_ascii=False).replace("<", "\\u003c"))
