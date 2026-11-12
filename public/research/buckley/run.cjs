'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const series=fs.readFileSync(__dirname+'/buckley-1250-1450.csv','utf8').trim().split('\n').slice(1).map(line=>line.split(',').map(Number));
assert.equal(series.length,201);
for(let i=0;i<series.length;i++)assert.equal(series[i][0],1250+i);
const pdsi=Object.fromEntries(series);
const source=fs.readFileSync(__dirname+'/longrun-source.js','utf8');
const original='const w = Math.min(1.15, (dry ? p.droughtMean : 1) + p.noise * (wr() + wr() + wr() - 1.5));';
assert.ok(source.includes(original));
const patched=source.replace(original, `const originalWeather = Math.min(1.15, (dry ? p.droughtMean : 1) + p.noise * (wr() + wr() + wr() - 1.5));
      const w = year >= 1250 ? Math.max(.4, Math.min(1.15, 1 + (neutral ? 0 : pdsi[year]) * sensitivity)) : originalWeather;`);
function engine(sensitivity,neutral){
 const ctx=vm.createContext({process:{env:{}},pdsi,sensitivity,neutral});
 vm.runInContext(patched,ctx);return ctx.AngkorStandard;
}
const reference=engine(0,true), rnd=reference.rngFrom(20261106);
const priors=Array.from({length:2000},(_,i)=>reference.drawPriors(rnd,1000+i));
const runs=[];
for(const sensitivity of [0,.04,.07,.10]){
 const A=engine(sensitivity,sensitivity===0);
 for(const p of priors){
  const rows=A.run(p,{}),s=A.score(rows);
  assert.ok(rows.every(r=>Number.isFinite(r.P)&&r.P>=0&&r.C>=0&&r.C<=1+1e-9));
  const at=y=>rows[y-A.FIRST];
  runs.push({sensitivity,seed:p.seed,onset:s.onset??'',moatLost:s.moatLost??'',
    core1300:at(1300).core,core1400:at(1400).core,core1450:at(1450).core,
    core1450_vs1300:at(1450).core/at(1300).core,
    regional1450_vs1300:at(1450).P/at(1300).P,
    channels1450:at(1450).C,peakYear:s.peakYear});
 }
}
const keys=Object.keys(runs[0]);
process.stdout.write([keys.join(','),...runs.map(r=>keys.map(k=>r[k]).join(','))].join('\n')+'\n');
