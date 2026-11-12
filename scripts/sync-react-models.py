"""Copy canonical browser models and translations into the React adapter, without equation edits."""
from pathlib import Path
import json,shutil,hashlib,re
root=Path(__file__).resolve().parents[1];public=root/'public';legacy=root/'src/models';legacy.mkdir(exist_ok=True)
files=['engines/atlas_data.js','engines/youth.js','engines/camchild.js','engines/lab_models.js','reference/angkor/model.js','engines/campaign.js','engines/signalling.js','engines/obligations.js','engines/monsoon.js','engines/relocation.js','engines/petri.js','engines/provisioning.js','evidence.js','worlds.js','engines/institution-data.js','institution-worlds.js']
imports=[]
for f in files:
 name='angkor-model.js' if f=='reference/angkor/model.js' else Path(f).name
 shutil.copyfile(public/f,legacy/name);imports.append("import './"+name+"'")
# Actual executable files are unmodified; hashes identify those copies.
p=legacy/'institution-data.js'
s=p.read_text();data=json.loads(s.split('=',1)[1].strip().rstrip(';'));p.write_text('globalThis.AngkorInstitutionData=JSON.parse('+json.dumps(json.dumps(data,separators=(',',':')))+');\n')
source={('model.js' if f=='reference/angkor/model.js' else Path(f).name):hashlib.sha256((public/f).read_bytes()).hexdigest() for f in files}
source['institution-data.js']=hashlib.sha256((legacy/'institution-data.js').read_bytes()).hexdigest()
s=(public/'evidence.js').read_text();declared=json.JSONDecoder().raw_decode(s[s.index('{'):])[0]['sha256']
for k,v in declared.items():source.setdefault(k,v)
(legacy/'source-hashes.json').write_text(json.dumps(source,indent=2))
(legacy/'index.ts').write_text('\n'.join(imports)+"\nimport type { World } from '../types'\nimport actualHashes from './source-hashes.json'\nexport const worlds = (globalThis as unknown as {AtlasWorldsLab:{worlds:World[]}}).AtlasWorldsLab.worlds\nexport const sourceHashes: Record<string,string> = actualHashes\n")
s=(public/'languages.js').read_text();a=s.index('const translations = ')+21;d=json.JSONDecoder().raw_decode(s[a:])[0]
(root/'src/data/translations.json').write_text(json.dumps(d,ensure_ascii=False,indent=2))
# Preserve the current published sequence, including the economic foundation.
s=(root/'tests/fixtures/classic-controller.js').read_text();a=s.index('const guideSteps = ')+len('const guideSteps = ');guide=json.JSONDecoder().raw_decode(s[a:])[0];(root/'src/data/guide.json').write_text(json.dumps(guide,ensure_ascii=False,indent=2))
