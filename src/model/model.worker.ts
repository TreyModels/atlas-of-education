/// <reference lib="webworker" />
import { worlds } from '../models'
import {comparisonFor} from '../lib/comparison'
import type { Values } from '../types'
const cache = new Map<string, unknown>()
self.onmessage = (event: MessageEvent<{id:number;world:string;values:Values}>) => {
 const {id,world:worldId,values}=event.data
 try {
  const world=worlds.find(w=>w.id===worldId)
  if(!world)throw new Error('Unknown model')
  const comparison=comparisonFor(world,values)
  const reference=comparison.referenceControls
  const key=worldId+JSON.stringify(reference)
  if(!cache.has(key))cache.set(key,world.run(reference))
  const baseline=cache.get(key)
  const current=JSON.stringify(reference)===JSON.stringify(values)?baseline:world.run(values)
  // JSON is also the export format; discard any incidental functions before posting.
  self.postMessage(JSON.parse(JSON.stringify({id,current,baseline,reference,values,comparison})))
 } catch(error){self.postMessage({id,error:error instanceof Error?error.message:String(error)})}
}
