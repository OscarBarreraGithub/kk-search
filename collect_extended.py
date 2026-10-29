from collect_kk import BASE,fetch,batch,Links
import re,json,urllib.parse,concurrent.futures

pages={
 'ATLAS_EXOT-2018-49':'https://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/PAPERS/EXOT-2018-49/index.php',
 'CMS_EXO-24-038':'https://cms-results.web.cern.ch/cms-results/public-results/publications/EXO-24-038/'
}
for p in (BASE/'papers').glob('*_metadata.html'):
 parser=Links();parser.feed(p.read_text())
 for u in parser.links:
  if 'cms-results.web.cern.ch/' in u or '/PHYSICS/PAPERS/' in u:
   u=u.replace('http:','https:').rstrip('/')+'/'
   key=('CMS_' if 'cms-results' in u else 'ATLAS_')+u.rstrip('/').rsplit('/',1)[-1]
   if 'ATLAS_' in key:u+='index.php'
   pages[key]=u

def page(kv):
 k,u=kv;r=fetch(u,f'analyses/{k}/index.html','results-page')
 if r['status']=='failed':return k,[]
 parser=Links();parser.feed((BASE/r['path']).read_text(errors='replace'))
 links=sorted(set(urllib.parse.urljoin(u,h) for h in parser.links))
 (BASE/f'analyses/{k}/links.json').write_text(json.dumps(links,indent=2))
 return k,links

alllinks={}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
 for k,links in ex.map(page,pages.items()):
  alllinks[k]=links
  print(k,'LINKS',len(links),'DATA',[u for u in links if 'hepdata' in u],flush=True)
(BASE/'extended_analysis_pages.json').write_text(json.dumps(pages,indent=2))
tasks=[]
for k,links in alllinks.items():
 prefix=pages[k].removesuffix('index.php')
 for u in links:
  if u.startswith(prefix) and re.search(r'\.(pdf|root|json|yaml|csv|C|zip)$',u):
   tasks.append((u,f'analyses/{k}/assets/{u.rsplit("/",1)[-1]}','analysis-asset'))
tasks.append(('https://arxiv.org/pdf/2507.17884v2','papers/2507.17884v2.pdf','paper'))
print('TASKS',len(tasks),flush=True)
batch(tasks,workers=8)
