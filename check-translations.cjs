const fs=require('fs'),vm=require('vm'),path=require('path');
const root=path.join(__dirname,'public');const c=vm.createContext({});
for(const [,file]of fs.readFileSync(__dirname+'/tests/fixtures/model-loader.html','utf8').matchAll(/<script defer src="([^"]+)"/g)){if(['app.js','languages.js'].includes(file))continue;vm.runInContext(fs.readFileSync(root+'/'+file,'utf8'),c);}
const source=fs.readFileSync(root+'/languages.js','utf8');const dict=JSON.parse(source.slice(source.indexOf('const translations = ')+21,source.indexOf(' ;\n const originals')));
const seen=new Set();const add=s=>{if(typeof s==='string'&&/[A-Za-z]{3}/.test(s)&&!dict[s])seen.add(s);};
for(const w of c.AtlasWorldsLab.worlds){[w.nav,w.title,w.meta,w.question].forEach(add);for(const f of w.controls){add(f.label);add(f.note);Object.values(f.options||{}).forEach(add);}for(const [label] of w.links)add(label);for(const x of typeof w.evidence==='function'?w.evidence(w.defaults):w.evidence){add(x.title);add(x.body);}const r=w.run(w.defaults),v=w.view(r,r);add(v.heading);add(v.note);for(const m of v.metrics){add(m.label);add(m.detail);}for(const l of v.lines||[])add(l.name);if(v.band)add(v.band.name);if(v.table){v.table.head.forEach(add);for(const r of v.table.rows)add(r.cells[0]);}}
console.log([...seen].join('\n'));
const assert=require('node:assert/strict');
const missing=[...seen].filter(s=>!['Lieberman & Buckley 2012','Buckley et al. 2010'].includes(s)&&!/^Teachers in \d+$/.test(s));
assert.deepEqual(missing,[],'Every model label, description, option and evidence note needs a translation');
// Exercise language switching, rerendered labels, option text and accessible attributes.
const records=['Regional population across seeds','Failed · Angkor as leading centre','Angkor across 100 seeds','High climate shock'].map(t=>({nodeValue:t,parentElement:{closest:()=>null}}));
let change;const selector={value:'en',addEventListener:(event,fn)=>change=fn};let languageAttr='Choose a model';
const element={id:'world-nav',hasAttribute:n=>n==='aria-label',getAttribute:()=>languageAttr,setAttribute:(_,v)=>languageAttr=v};
const dom={documentElement:{},body:{},getElementById:()=>selector,createTreeWalker:()=>{let i=0;return{nextNode:()=>records[i++]||null};},querySelectorAll:()=>[element]};
let observe;class Observer{constructor(fn){observe=fn;}disconnect(){}observe(){}}
const context=vm.createContext({document:dom,NodeFilter:{SHOW_TEXT:4},MutationObserver:Observer,localStorage:{getItem:()=>null,setItem:()=>{}}});
vm.runInContext(source,context);
for(const lang of ['zh-Hans','fr','vi','en']){selector.value=lang;change();assert.equal(records[0].nodeValue,lang==='en'?'Regional population across seeds':dict['Regional population across seeds'][lang]);assert.equal(dom.documentElement.lang,lang);}
selector.value='zh-Hans';change();records[0].nodeValue='Median population in 1500';observe();assert.equal(records[0].nodeValue,dict['Median population in 1500']['zh-Hans']);assert.equal(languageAttr,'选择模型');
console.log('Translation coverage and language-switch checks passed.');

for (const [key, value] of Object.entries(dict)) assert.ok(typeof value.vi === 'string' && value.vi.trim(), 'Missing Vietnamese: '+key);
selector.value='vi';change();assert.equal(context.AtlasI18n.text('Teachers in 2050'),'Giáo viên năm 2050');assert.equal(context.AtlasI18n.text('In 1200 CE'),'Năm 1200 CN');assert.equal(context.AtlasI18n.text('40 days'),'40 ngày');assert.equal(context.AtlasI18n.text('Failed · Angkor as leading centre'),dict['Failed · Angkor as leading centre'].vi);
assert.ok(fs.readFileSync(__dirname+'/tests/fixtures/model-loader.html','utf8').includes('<option value="vi">Tiếng Việt</option>'));
const queryContext=vm.createContext({document:dom,NodeFilter:{SHOW_TEXT:4},MutationObserver:Observer,URLSearchParams,location:{search:'?lang=vi'},localStorage:{getItem:()=> 'en',setItem:()=>{}}});vm.runInContext(source,queryContext);assert.equal(dom.documentElement.lang,'vi');console.log('Vietnamese: all entries, dynamic labels and direct language link passed.');
