import type { Translate } from '../types'
import type { CatalogueItem } from '../data/model-catalogue'
import { familyInfo } from '../data/model-catalogue'

/**
 * Shared query matcher for the catalogue: the Find-a-model modal and the
 * Library search both use it, so `#tag` queries behave identically.
 *
 * Rules:
 * - Tokens beginning with `#` are hashtag filters. They match a tag exactly,
 *   by prefix, or as a substring, and several tags are ANDed together.
 * - Every other token matches the entry's text, its tags, or the translated
 *   text, and all plain tokens must match (AND).
 * - Hashtags stay Latin in every language; only the chrome is translated.
 */
export function parseTags(raw: string): string[] {
  const tags: string[] = []
  for (const match of raw.toLowerCase().matchAll(/#([a-z0-9-]+)/g)) tags.push(match[1])
  return [...new Set(tags)]
}

export function stripTags(raw: string): string {
  return raw.replace(/#[a-z0-9-]+/gi, ' ').replace(/\s+/g, ' ').trim()
}

export function hasQuery(raw: string): boolean {
  return stripTags(raw).length > 0 || parseTags(raw).length > 0
}

function tagMatches(tag: string, needle: string): boolean {
  return tag === needle || tag.startsWith(needle) || tag.includes(needle)
}

/** Append a tag to a query, keeping any words the user already typed. */
export function addTag(raw: string, tag: string): string {
  const clean = tag.replace(/^#/, '')
  return [stripTags(raw), `#${clean}`].filter(Boolean).join(' ')
}

/** Remove a tag from a query, keeping the other words and tags. */
export function removeTag(raw: string, tag: string): string {
  return raw
    .replace(new RegExp(`#${tag.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}(?![a-z0-9-])`, 'gi'), ' ')
    .replace(/\s+/g, ' ')
    .trim()
}

export function matchesQuery(item: CatalogueItem, rawQuery: string, t: Translate): boolean {
  const tags = parseTags(rawQuery)
  const words = stripTags(rawQuery).toLowerCase().split(/\s+/).filter(Boolean)
  if (!tags.length && !words.length) return true
  if (!tags.every(needle => item.tags.some(tag => tagMatches(tag, needle)))) return false
  if (!words.length) return true
  const info = familyInfo[item.family]
  const haystack = [
    item.title, item.question, item.method, item.format, item.keywords ?? '',
    item.family, item.tags.join(' '), `#${item.tags.join(' #')}`,
    t(item.title), t(item.question), t(item.method), t(item.format),
    t(info.short), t(info.title),
  ].join(' ').toLowerCase()
  return words.every(word => haystack.includes(word))
}
