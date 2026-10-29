#!/usr/bin/env python3
"""Collect public sources for arXiv:2610.31458. No credentials required."""
import concurrent.futures as cf
import datetime, hashlib, json, pathlib, re, threading, urllib.request, urllib.parse
from html.parser import HTMLParser

BASE=pathlib.Path(__file__).parent/'kk_data_access_2026-10-28'
BASE.mkdir(exist_ok=True)
LOCK=threading.Lock()
LOG=BASE/'download_log.jsonl'

def fetch(url, rel, kind='source', max_bytes=50_000_000):
    path=BASE/rel
    item={'url':url,'path':str(rel),'kind':kind,'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        if path.exists():
            data=path.read_bytes(); item['status']='cached'
        else:
            req=urllib.request.Request(url,headers={'User-Agent':'ResearchDataInventory/1.0','Accept':'*/*'})
            with urllib.request.urlopen(req,timeout=40) as r:
                item.update(http_status=r.status,content_type=r.headers.get('Content-Type'),resolved_url=r.url)
                if int(r.headers.get('Content-Length') or 0)>max_bytes: raise ValueError('size exceeds per-file collection limit')
                data=r.read(max_bytes+1)
                if len(data)>max_bytes: raise ValueError('size exceeds per-file collection limit')
            if str(rel).endswith('.pdf') and not data.startswith(b'%PDF'): raise ValueError('not a PDF')
            if str(rel).endswith('.json'): json.loads(data)
            if str(rel).endswith('.tar.gz') and not data.startswith(b'\x1f\x8b'): raise ValueError('not a gzip archive')
            path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(data); item['status']='downloaded'
        item.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
    except Exception as e:
        item.update(status='failed',error=str(e))
    with LOCK:
        with LOG.open('a') as f:f.write(json.dumps(item)+'\n')
    return item

def batch(tasks,workers=6):
    with cf.ThreadPoolExecutor(max_workers=workers) as pool:
        for result in pool.map(lambda t:fetch(*t),tasks):
            print(json.dumps({k:result[k] for k in ['path','status','bytes','error'] if k in result}),flush=True)

class Links(HTMLParser):
    def __init__(self):super().__init__(); self.links=[]
    def handle_starttag(self,tag,attrs):
        if tag=='a':
            d=dict(attrs)
            if d.get('href'):self.links.append(d['href'])

PAPERS=['2610.31458v2','2206.09997v3','2307.14944v2','2609.21850','2610.05889','2606.29922','2506.09490','hep-ph/0701186','2607.12012','hep-ph/0104002','1603.06980','hep-ph/0701166','hep-ph/0610173','2210.00043v2','1905.00220','0709.0007','2512.17856','hep-ph/0305086','1808.03124']
PAGES={
 'CMS_EXO-21-010':'https://cms-results.web.cern.ch/cms-results/public-results/publications/EXO-21-010/',
 'CMS_EXO-25-004':'https://cms-results.web.cern.ch/cms-results/public-results/preliminary-results/EXO-25-004/',
 'CMS_EXO-24-039':'https://cms-results.web.cern.ch/cms-results/public-results/publications/EXO-24-039/',
 'CMS_B2G-20-009':'https://cms-results.web.cern.ch/cms-results/public-results/publications/B2G-20-009/',
 'CMS_EXO-25-021':'https://cms-results.web.cern.ch/cms-results/public-results/preliminary-results/EXO-25-021/',
 'CMS_EXO-17-021':'https://cms-results.web.cern.ch/cms-results/public-results/publications/EXO-17-021/',
 'ATLAS_EXOT-2022-18':'https://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/PAPERS/EXOT-2022-18/',
}

if __name__=='__main__':
    import sys
    mode=sys.argv[1] if len(sys.argv)>1 else 'initial'
    if mode=='initial':
        tasks=[(f'https://arxiv.org/pdf/{p}',f'papers/{p.replace("/","_")}.pdf','paper') for p in PAPERS]
        tasks += [(u,f'analyses/{k}/index.html','results-page') for k,u in PAGES.items()]
        batch(tasks)
    elif mode=='assets':
        tasks=[]; discovered={}
        for key,url in PAGES.items():
            path=BASE/f'analyses/{key}/index.html'
            if not path.exists():continue
            parser=Links(); parser.feed(path.read_text(errors='replace'))
            links=sorted(set(urllib.parse.urljoin(url,h) for h in parser.links))
            discovered[key]=links
            for link in links:
                name=urllib.parse.urlparse(link).path.rsplit('/',1)[-1]
                if link.startswith(url) and re.search(r'\.(pdf|root|json|yaml|yml|csv|txt|C|tar\.gz|zip)$',name):
                    tasks.append((link,f'analyses/{key}/assets/{name}','analysis-asset'))
                elif 'cds.cern.ch/record/' in link and link.endswith('.pdf'):
                    tasks.append((link,f'analyses/{key}/report.pdf','analysis-report'))
        (BASE/'discovered_links.json').write_text(json.dumps(discovered,indent=2))
        print('ASSET_TASKS',len(tasks),flush=True); batch(tasks,workers=8)
