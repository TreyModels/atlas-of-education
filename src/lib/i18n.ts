import translations from '../data/translations.json'
import ui from '../data/ui-translations.json'
import type { Language } from '../types'
const dictionary:Record<string,Partial<Record<Language,string>>>={...translations,...ui}
const keys=Object.keys(dictionary).sort((a,b)=>b.length-a.length)
export function translate(source:string,language:Language):string {
 if(language==='en')return source
 if(dictionary[source]?.[language])return dictionary[source][language]!
 const labels={ 'zh-Hans':{teachers:'年教师人数',year:'公元',ce:'年',days:' 天',years:' 年',perYear:'吨/年',eq:'吨当量'},fr:{teachers:'Enseignants en ',year:'En ',ce:' de notre ère',days:' jours',years:' ans',perYear:'t/an',eq:'t éq.'},vi:{teachers:'Giáo viên năm ',year:'Năm ',ce:' CN',days:' ngày',years:' năm',perYear:'tấn/năm',eq:'tấn tương đương'}}[language]
 if(/^Teachers in \d+$/.test(source))return source.replace(/^Teachers in (\d+)$/,(_,y)=>language==='zh-Hans'?y+labels.teachers:labels.teachers+y)
 if(/^In \d+ CE$/.test(source))return source.replace(/^In (\d+) CE$/,(_,y)=>labels.year+y+labels.ce)
 let result=source
 for(const key of keys)if(key.length>=5&&result.includes(key)&&dictionary[key][language])result=result.split(key).join(dictionary[key][language]!)
 result=result.replace(/(\d[\d,.]*) days\b/g,(_,n)=>n+labels.days).replace(/(\d[\d,.]*) yr\b/g,(_,n)=>n+labels.years)
 result=result.replace(/\bt\/yr\b/g,labels.perYear).replace(/\bt eq\./g,labels.eq)
 if(/^(\d[\d,]*) of 24,000$/.test(source))return source.replace(/^(\d[\d,]*) of 24,000$/,(_,n)=>language==='fr'?n+' sur 24 000':n+' / 24.000')
 return result
}
export const supportedLanguages:Language[]=['en','zh-Hans','vi']
export const translationDictionary=dictionary
