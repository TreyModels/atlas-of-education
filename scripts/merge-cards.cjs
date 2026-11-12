const fs=require('fs'),vm=require('vm'),path=require('path');const root=path.join(__dirname,'..');const c=vm.createContext({});for(const [,f]of fs.readFileSync(root+'/tests/fixtures/model-loader.html','utf8').matchAll(/<script defer src="([^"]+)"/g))if(!['app.js','languages.js'].includes(f))vm.runInContext(fs.readFileSync(root+'/public/'+f,'utf8'),c);
const cards=JSON.parse(fs.readFileSync(root+'/src/data/cards.json'));const notes={
provisioning:['The curve is a normalized output index. The historical sample is shown in the cookbook; it records buildup without simulating it.','research/provisioning.html'],
petri:['The model is a mechanism test. It has no historical fit score and no claim to identify the cause of Angkor’s decline.','research/provisioning.html'],
relocation:['A court can leave while farming and local maintenance continue. Movement rules remain experimental assumptions.','research/relocation.html'],
institutions:['Food access differs under assumed relief and extraction rules. Each scenario is one trial.','research/institutions/index.html'],
flight:['State-linked and refuge populations follow separate trajectories under assumed movement rules.','research/institutions/index.html'],
maintenance:['The corrected maintenance-only drought median is 6,209 state-linked people; its unchanged stable reference is 6,958.','research/institutions/index.html'],
accounts:['The extension checks annual grain, population and labour balances. Historical rates remain uncalibrated.','research/institutions/index.html']};
for(const [id,[note,research]]of Object.entries(notes)){const w=c.AtlasWorldsLab.worlds.find(w=>w.id===id);if(cards.some(c=>c.href==='#'+id))continue;cards.push({eyebrow:w.meta,title:w.title,question:w.question,href:'#'+id,badge:'Under active examination',research,details:[{term:'What we tested',description:w.question},{term:'What we learned',description:note}]});}
cards.sort((a,b)=>(a.href==='#provisioning'?-1:b.href==='#provisioning'?1:0));fs.writeFileSync(root+'/src/data/cards.json',JSON.stringify(cards,null,2));
console.log('Cards',cards.length,'models',c.AtlasWorldsLab.worlds.length)
