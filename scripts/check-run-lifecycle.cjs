const assert=require('node:assert/strict'),fs=require('fs'),vm=require('vm'),esbuild=require('esbuild');
let slots=[],cursor=0,effects=[],deps=[],cleanups=[],workers=[],failStartup=false;
const equal=(a,b)=>a&&b&&a.length===b.length&&a.every((v,i)=>Object.is(v,b[i]));
const react={useState(initial){const i=cursor++;if(!(i in slots))slots[i]=initial;return [slots[i],v=>slots[i]=typeof v==='function'?v(slots[i]):v]},useRef(initial){const i=cursor++;return slots[i]??(slots[i]={current:initial})},useEffect(fn,d){const i=cursor++;if(!equal(deps[i],d)){effects.push(()=>{cleanups[i]?.();cleanups[i]=fn()});deps[i]=d}}};
class FakeWorker{constructor(){if(failStartup)throw Error('blocked worker');workers.push(this);this.requests=[]}postMessage(r){this.requests.push(r)}terminate(){this.terminated=true}finish(r,error){this.onmessage({data:error?{id:r.id,error}:{...r,current:{},baseline:{},reference:{}}})}}
let code=fs.readFileSync('src/model/useModelRun.ts','utf8').replace("new URL('./model.worker.ts',import.meta.url)","'worker.js'");code=esbuild.transformSync(code,{loader:'ts',format:'cjs'}).code;
const box={module:{exports:{}},require:()=>react,Worker:FakeWorker,setTimeout:()=>1,clearTimeout(){}};vm.runInNewContext(code,box);const hook=box.module.exports.useModelRun;
let values={x:1};function render(){cursor=0;const out=hook('test',values);const pending=effects;effects=[];pending.forEach(f=>f());return out}
render();let w=workers.at(-1);assert.equal(w.requests.length,1);
values={x:2};render();values={x:3};render();assert.equal(w.requests.length,1,'intermediate positions coalesced');w.finish(w.requests[0]);assert.equal(w.requests.length,2);assert.equal(w.requests[1].values.x,3);w.finish(w.requests[1]);let out=render();assert.equal(out.pending,false);assert.equal(out.result.values.x,3);
out.recompute();render();assert.equal(w.terminated,true);w=workers.at(-1);assert.equal(w.requests.length,1,'manual recompute starts fresh engine');w.onerror();out=render();assert.ok(out.error);assert.ok(out.result,'previous completed results retained on error');out.recompute();render();w=workers.at(-1);w.finish(w.requests[0]);out=render();assert.equal(out.error,null);assert.equal(out.pending,false);
cleanups.forEach(f=>f?.());slots=[];deps=[];cleanups=[];failStartup=true;render();out=render();assert.ok(out.error,'startup errors recoverable');assert.equal(out.pending,false);
console.log('Worker queue, latest slider value, manual restart, failure recovery and blocked startup passed.');
