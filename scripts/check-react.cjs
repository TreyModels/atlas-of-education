const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('node:assert/strict'),ts=require('typescript');
const root=path.join(__dirname,'..');const context=vm.createContext({});
const original=fs.readFileSync(root+'/tests/fixtures/model-loader.html','utf8');
for(const [,file]of original.matchAll(/<script defer src="([^"]+)"/g))if(!['app.js','languages.js'].includes(file))vm.runInContext(fs.readFileSync(root+'/public/'+file,'utf8'),context);
const compile=(file,extras={})=>{const m={exports:{}};const code=ts.transpileModule(fs.readFileSync(file,'utf8'),{fileName:file,compilerOptions:{jsx:ts.JsxEmit.ReactJSX,target:ts.ScriptTarget.ES2022,module:ts.ModuleKind.CommonJS,esModuleInterop:true}}).outputText;const ctx=vm.createContext({module:m,exports:m.exports,require:p=>p.startsWith('.')?require(path.resolve(path.dirname(file),p)):require(p),...extras});vm.runInContext(code,ctx);return m.exports;};
const {translate:t,translationDictionary:dictionary}=compile(root+'/src/lib/i18n.ts');
const stories=require('../src/data/model-stories.json');assert.equal(Object.keys(stories).length,22);const audit=require('../src/data/control-audit.json');assert.equal(Object.keys(audit.models).length,22);
const all=new Set();const add=s=>{if(typeof s==='string'&&/[A-Za-z]{3}/.test(s))all.add(s)};
for(const file of ['App.tsx','components/Library.tsx','components/Navigation.tsx','components/ModelNavigator.tsx','components/Guide.tsx','components/Workbench.tsx','components/DataChart.tsx','components/ModelQuestions.tsx','components/ModelNarrative.tsx']){
 const text=fs.readFileSync(root+'/src/'+file,'utf8');for(const m of text.matchAll(/\bt\('([^']*)'\)/g))add(m[1]);
}
for(const c of JSON.parse(fs.readFileSync(root+'/src/data/cards.json'))){[c.title,c.question,c.eyebrow,c.badge,...c.details.flatMap(d=>[d.term,d.description])].forEach(add)}
const catalogueSource=fs.readFileSync(root+'/src/data/model-catalogue.ts','utf8');
for(const m of catalogueSource.matchAll(/(?:title|question|method|short|description|label): '([^']+)'/g))add(m[1]);
for(const m of catalogueSource.matchAll(/external\('[^']+', '[^']+', '([^']+)', '([^']+)', '([^']+)'/g))m.slice(1).forEach(add);
for(const m of catalogueSource.matchAll(/internal\('[^']+', '[^']+', '([^']+)'\)/g))add(m[1]);
['Atlas workbench','Classic workbench'].forEach(add);
for(const step of JSON.parse(fs.readFileSync(root+'/src/data/guide.json')))step.slice(1).forEach(add);
for(const w of context.AtlasWorldsLab.worlds){
 [w.nav,w.title,w.meta,w.question].forEach(add);for(const f of w.controls){[f.label,f.note,...Object.values(f.options||{})].forEach(add)}
 const r=w.run(w.defaults),v=w.view(r,r);add(v.heading);add(v.note);v.metrics.forEach(m=>[m.label,m.detail].forEach(add));v.lines?.forEach(l=>add(l.name));
 for(const e of typeof w.evidence==='function'?w.evidence(w.defaults):w.evidence)[e.title,e.body].forEach(add);w.links.forEach(l=>add(l[0]));
}
Object.values(stories).forEach(add);Object.values(require('../src/data/analysis-advice.json')).forEach(add);
for(const w of context.AtlasWorldsLab.worlds){assert.ok(stories[w.id]);for(const control of w.controls)assert.ok(audit.models[w.id].controls[control.key]);}
const exempt=new Set(['Lieberman & Buckley 2012','Buckley et al. 2010']);
let missing=[];for(const text of all)if(!dictionary[text]&&!exempt.has(text)&&!/^Teachers in \d+$/.test(text))missing.push(text);
if(missing.length){console.log('Missing exact React translation entries:',JSON.stringify(missing,null,2));process.exitCode=1;}
for(const [key,v]of Object.entries(dictionary))for(const lang of ['vi','zh-Hans','fr'])assert.ok(v[lang]?.trim(),lang+': '+key);
for(const lang of ['vi','zh-Hans','fr'])for(const text of all)assert.ok(!t(text,lang).includes('undefined'),lang+': '+text);
assert.equal(t('Teachers in 2050','vi'),'Giáo viên năm 2050');assert.equal(t('40 days','vi'),'40 ngày');
assert.equal(context.AtlasWorldsLab.worlds.length,22);assert.ok(fs.readFileSync(root+'/src/components/Navigation.tsx','utf8').includes('<option value="vi">Tiếng Việt</option>'));
assert.ok(fs.readFileSync(root+'/src/model/useModelRun.ts','utf8').includes('latest.current=request'));
console.log('React: 22 modules, '+Object.keys(dictionary).length+' translated entries, Vietnamese dynamic labels and selector checked.');

const React=require('react'),{renderToStaticMarkup}=require('react-dom/server');const {ModelNarrative,trials}=compile(root+'/src/components/ModelNarrative.tsx');const {ModelQuestions}=compile(root+'/src/components/ModelQuestions.tsx');
for(const w of context.AtlasWorldsLab.worlds){
 const r=w.run(w.defaults),v=w.view(r,r);for(const [k,x] of Object.entries(trials[w.id])){const c=w.controls.find(c=>c.key===k);assert.ok(c);if(c.options)assert.ok(c.options[x]);else assert.ok(x>=c.min&&x<=c.max);}
 for(const lang of ['en','vi','zh-Hans','fr']){const translate=s=>t(String(s),lang);const html=renderToStaticMarkup(React.createElement(ModelNarrative,{world:w,view:v,referenceView:v,values:w.defaults,onChange:()=>{},t:translate,pending:false}));assert.ok(!html.includes('undefined'));assert.ok(html.includes('story-intro'));const answers=renderToStaticMarkup(React.createElement(ModelQuestions,{world:w,values:w.defaults,view:v,t:translate}));assert.equal((answers.match(/<details>/g)||[]).length,4);assert.ok(!answers.includes('undefined'));}
}
console.log('All 22 introductions, bounded trial actions and model-specific answers render in four languages.');
