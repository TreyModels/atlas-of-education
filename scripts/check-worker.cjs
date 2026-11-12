const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('node:assert/strict'),{Worker}=require('node:worker_threads');
const root=path.join(__dirname,'..'),ctx=vm.createContext({});
for(const [,f]of fs.readFileSync(root+'/tests/fixtures/model-loader.html','utf8').matchAll(/<script defer src="([^"]+)"/g))if(!['app.js','languages.js'].includes(f))vm.runInContext(fs.readFileSync(root+'/public/'+f,'utf8'),ctx);
const file=fs.readdirSync(root+'/dist/assets').find(f=>f.startsWith('model.worker-')&&f.endsWith('.js'));
const code=fs.readFileSync(root+'/dist/assets/'+file,'utf8');
const w=new Worker(`const {parentPort}=require('node:worker_threads');const vm=require('node:vm');const box=vm.createContext({self:{postMessage:x=>parentPort.postMessage(x)}});vm.runInContext(${JSON.stringify(code)},box,{filename:'browser-worker.js'});parentPort.on('message',data=>box.self.onmessage({data}));`,{eval:true});
let counter=0;
function request(world,values){return new Promise((resolve,reject)=>{const id=++counter;const failed=e=>{w.removeListener('message',done);reject(e)};const done=r=>{w.removeListener('error',failed);r.id===id?resolve(r):reject(new Error('Unexpected response id'))};w.once('message',done);w.once('error',failed);w.postMessage({id,world,values});});}
(async()=>{try{
 for(const world of ctx.AtlasWorldsLab.worlds){
  const r=await request(world.id,world.defaults);assert.ok(!r.error,r.error);assert.equal(JSON.stringify(r.current),JSON.stringify(world.run(world.defaults)),world.id+' worker parity');assert.equal(JSON.stringify(r.values),JSON.stringify(world.defaults));
  // Exercise the same view and export paths React uses after a worker message.
  const view=world.view(r.current,r.baseline);assert.ok(view.metrics.length>0);
  if(world.csv)assert.ok(world.csv(r.current).includes('\n'));
  console.log(world.id+': built worker matches canonical output');
 }
 for(const [id,patch]of [['campaign',{distance:540}],['accounts',{scenario:'reshuffle',climate:'drought',draw:39}],['provisioning',{community:500}]]){
  const world=ctx.AtlasWorldsLab.worlds.find(w=>w.id===id),values={...world.defaults,...patch};const r=await request(id,values);assert.ok(!r.error,r.error);assert.equal(JSON.stringify(r.current),JSON.stringify(world.run(values)),id+' changed controls');
 }
 const r=await request('unknown',{});assert.equal(r.error,'Unknown model');console.log('22 default models, 3 changed inputs, CSV views and worker error path passed.');
}finally{await w.terminate();}})().catch(e=>{console.error(e.message);process.exitCode=1});
