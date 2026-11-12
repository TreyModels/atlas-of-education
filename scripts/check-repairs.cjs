const fs=require('fs'),vm=require('vm'),path=require('path'),assert=require('node:assert/strict'),ts=require('typescript');
const root=path.join(__dirname,'..');const load=f=>{const m={exports:{}};vm.runInNewContext(ts.transpileModule(fs.readFileSync(root+'/'+f,'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2022}}).outputText,{module:m,exports:m.exports});return m.exports};
const nav=load('src/lib/navigation.ts'),{comparisonFor}=load('src/lib/comparison.ts');
for(const model of ['campaign','accounts','china',''])for(const section of nav.sections){assert.equal(nav.parseLocation(nav.sectionHash(model,section)).route,model);assert.equal(nav.parseLocation(nav.sectionHash(model,section)).section,section)}
const preserved=nav.preserveHandoff({disruption:.65,returnRule:'closed'},{disruption:.2,returnRule:'open'},{seed:44,loss:.8});assert.equal(preserved.disruption,.2);assert.equal(preserved.returnRule,'open');assert.equal(preserved.upstream.loss,.8);
const c=vm.createContext({});for(const [,f]of fs.readFileSync(root+'/tests/fixtures/model-loader.html','utf8').matchAll(/<script defer src="([^"]+)"/g))if(!['app.js','languages.js'].includes(f))vm.runInContext(fs.readFileSync(root+'/public/'+f,'utf8'),c);
const hashes=require('../src/models/source-hashes.json');for(const w of c.AtlasWorldsLab.worlds)for(const file of w.engines)assert.match(hashes[file],/^[a-f0-9]{64}$/,'Missing '+w.id+' '+file);
for(const id of ['maintenance','accounts','flight'])for(const climate of ['normal','drought'])for(const draw of [0,39]){
 const w=c.AtlasWorldsLab.worlds.find(w=>w.id===id),p={...w.defaults,climate,draw};const spec=comparisonFor(w,p);assert.equal(spec.referenceControls.climate,climate);assert.equal(spec.referenceControls.draw,draw);const current=w.run(p),reference=w.run(spec.referenceControls);assert.equal(JSON.stringify(current.baseline),JSON.stringify(reference.rows),id+' plotted baseline and narrative baseline must agree');
}
const zero=c.AngkorCampaign.compare({...c.AngkorCampaign.defaults,levy:0,collection:0,fightingDays:180,distance:540});assert.equal(zero.rows.filter(r=>r.campaignStarted).length,0);assert.ok(zero.campaignDays>120);
console.log('Routing/section identities, handoff preservation, all declared hashes, matched baseline trajectories and unfunded long campaign checks passed.');
