import type { ModelCard } from './angkor-journey'
import { journey as angkorJourney } from './angkor-journey'
import { educationJourney } from './education-journey'
import { systemsJourney } from './systems-journey'
import { planningJourney } from './planning-journey'
import { shadowJourney } from './shadow-journey'
import { fertilityJourney } from './fertility-journey'
import { deepHistoryJourney } from './deephistory-journey'
import { ccpJourney } from './ccp-journey'
import { extensionJourney } from './extension-journey'

/**
 * Every narrated model card, flattened by model id.
 *
 * The journey pages already carry the honest labels for each model (purpose,
 * development state, limitation note, source links). Reusing that single source
 * on the workbench page keeps the model card and the family story in sync
 * instead of growing a second set of labels that can drift.
 */
export const journeyModels: Record<string, ModelCard> = {
  ...angkorJourney.models,
  ...educationJourney.models,
  ...systemsJourney.models,
  ...planningJourney.models,
  ...shadowJourney.models,
  ...fertilityJourney.models,
  ...deepHistoryJourney.models,
  ...ccpJourney.models,
  ...extensionJourney.models,
}

export function modelCardFor(id: string): ModelCard | undefined {
  return journeyModels[id]
}
