import {useEffect,useRef,useState} from 'react'
import type {Comparison} from '../lib/comparison'
import type {Values} from '../types'
type Result={comparison?:Comparison;id:number;current:unknown;baseline:unknown;reference:Values;values:Values;error?:string}
// One active calculation and one replaceable pending request keep continuous
// slider input responsive without queuing every intermediate position.
export function useModelRun(world:string,values:Values){
 const [generation,restart]=useState(0)
 const [result,setResult]=useState<Result|null>(null)
 const [error,setError]=useState<string|null>(null)
 const [running,setRunning]=useState(true)
 const [runNumber,setRunNumber]=useState(0)
 const worker=useRef<Worker|null>(null),busy=useRef(false),latest=useRef<{id:number;world:string;values:Values}|null>(null),counter=useRef(0)
 useEffect(()=>{
  let alive=true
  let timer:ReturnType<typeof setTimeout>|undefined
  const fail=()=>{if(!alive)return;busy.current=false;latest.current=null;setRunning(false);setError('Unable to calculate this model. Use Retry calculation to restart the engine.');worker.current?.terminate();worker.current=null}
  const dispatch=(request:{id:number;world:string;values:Values})=>{
   busy.current=true;setRunning(true);clearTimeout(timer)
   timer=setTimeout(fail,120000)
   try{worker.current!.postMessage(request)}catch{fail()}
  }
  try{
   const w=new Worker(new URL('./model.worker.ts',import.meta.url),{type:'module'});worker.current=w
   w.onmessage=(event:MessageEvent<Result>)=>{
    if(!alive)return
    clearTimeout(timer);busy.current=false
    const response=event.data
    if(response.error){if(response.id===counter.current){setError(response.error);setRunning(false)}}
    else {setResult(response);setError(null);setRunNumber(n=>n+1);setRunning(false)}
    const next=latest.current;if(next){latest.current=null;dispatch(next)}
   }
   w.onerror=fail;w.onmessageerror=fail
   // Expose dispatch for subsequent changes only after worker setup succeeds.
   send.current=dispatch
  }catch{fail()}
  return()=>{alive=false;clearTimeout(timer);worker.current?.terminate();worker.current=null;busy.current=false;latest.current=null;send.current=null}
 },[world,generation])
 const send=useRef<((request:{id:number;world:string;values:Values})=>void)|null>(null)
 useEffect(()=>{
  if(!send.current)return
  setError(null)
  const request={id:++counter.current,world,values}
  if(busy.current)latest.current=request
  else if(send.current)send.current(request)
 },[world,values,generation])
 return {result,error,runNumber,recompute:()=>{setError(null);setRunning(true);restart(n=>n+1)},pending:running||(!error&&(!result||JSON.stringify(result.values)!==JSON.stringify(values)))}
}
