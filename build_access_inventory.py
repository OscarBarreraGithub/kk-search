#!/usr/bin/env python3
"""Normalize the collected public metadata without downloading event datasets."""
from pathlib import Path
import ast, collections, hashlib, json, urllib.parse, zlib

B=Path(__file__).parent/'kk_data_access_2026-10-28'
def write(p,obj):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,indent=2)+'\n')
def files_of(m):
    fs={}
    for i in m.get('_file_indices',[]):
        for f in i.get('files',[]):
            if f.get('uri'):fs[f['uri']]=f
    for f in m.get('files',[]):
        if f.get('uri'):fs[f['uri']]=f
    return list(fs.values())
def https(u):
    p=urllib.parse.urlparse(u)
    if p.scheme=='root' and p.hostname=='eospublic.cern.ch':
        return 'https://opendata.cern.ch/'+p.path.lstrip('/')
    return u if p.scheme=='https' else None

out=[];allfiles={}
for p in sorted((B/'opendata/records').glob('*.json'),key=lambda x:int(x.stem)):
    m=json.loads(p.read_text())['metadata'];rid=p.stem;fs=files_of(m)
    dist=m.get('distribution',{})
    rows=[]
    for f in fs:
        r={k:f.get(k) for k in ['filename','uri','size','checksum','availability']}
        r['record_id']=int(rid);r['https_url']=https(f['uri']);rows.append(r)
    mp=B/f'opendata/manifests/{rid}.jsonl';mp.parent.mkdir(exist_ok=True)
    mp.write_text(''.join(json.dumps(r)+'\n' for r in rows))
    (mp.with_suffix('.uris.txt')).write_text(''.join(r['uri']+'\n' for r in rows))
    allfiles[rid]=rows
    size=sum(f.get('size',0) for f in rows);root=[f for f in rows if '.root' in str(f['filename'])]
    issues=[]
    if dist.get('size') and dist['size']!=size:issues.append('Declared dataset size differs from sum of enumerated file sizes.')
    if dist.get('number_files') and dist['number_files']!=len(rows):issues.append('Declared file count differs from enumerated file count; may include auxiliary files.')
    out.append({'record_id':int(rid),'title':m['title'],'record_url':f'https://opendata.cern.ch/record/{rid}',
      'api_url':f'https://opendata.cern.ch/api/records/{rid}','doi':m.get('doi'),'license':m.get('license'),
      'published':m.get('date_published'),'created':m.get('date_created'),'run_period':m.get('run_period'),
      'distribution_as_published':dist,'enumerated_files':len(rows),'enumerated_root_files':len(root),'enumerated_bytes':size,
      'manifest':str(mp.relative_to(B)),'metadata':str(p.relative_to(B)),'issues':issues,
      'download_status':'metadata_and_file_manifest; only listed sample/auxiliary files are downloaded'})
write(B/'opendata/dataset_inventory.json',out)

validation=json.loads((B/'opendata/sample_validation.json').read_text())
brief=[]
for v in validation:
    rid=v['file'].split('_')[0];name=v['file'][len(rid)+1:];matches=[r for r in allfiles[rid] if r['uri'].rsplit('/',1)[-1]==name]
    assert len(matches)==1,(rid,name,len(matches))
    row=matches[0];actual='adler32:'+v['adler32']
    assert actual==row['checksum'],(actual,row['checksum'])
    assert v['bytes']==row['size']
    brief.append({'file':'opendata/samples/'+v['file'],'record_id':int(rid),'bytes':v['bytes'],'entries':v['entries'],
       'tree':v['tree'],'checksum_expected':row['checksum'],'checksum_actual':actual,'checksum_matches':True,
       'source':row['uri'],'https_url':row['https_url'],'verification':'ROOT file opened; tree entries and branches inspected'})
write(B/'opendata/validated_samples.json',brief)

src=B/'numerical/secondary_symbolfit/dataset.py'
vals={}
for n in ast.parse(src.read_text()).body:
    if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
        try: vals[n.targets[0].id]=ast.literal_eval(n.value)
        except (ValueError,TypeError): pass
needed=['x','y','y_up','y_down','bin_widths_1d']
assert all(len(vals[k])==44 for k in needed)
write(B/'numerical/secondary_symbolfit/inclusive_fourjet_44bins.json',{
 'provenance_status':'SECONDARY COPY. Not yet compared with the original HEPData export.',
 'source':'https://github.com/hftsoi/symbolfit/blob/d6c8bf035bedf30da4e8f4ae777dc6ca5c453cdf/examples/datasets/dijet_pair/dataset.py',
 'claimed_original':'https://www.hepdata.net/record/ins2098256',
 'figure':'CMS EXO-21-010 Figure 15, inclusive alpha > 0.1',
 'units':{'x':'GeV (values converted from TeV-axis plot in secondary source)','y':'pb/TeV, numerically equivalent to fb/GeV; assigned from official Figure 15 axis'},
 'bins':[{'center':vals['x'][i],'width':vals['bin_widths_1d'][i],'value':vals['y'][i],
          'uncertainty_up':vals['y_up'][i],'uncertainty_down':vals['y_down'][i]} for i in range(44)]})

primary={
 'CMS_EXO-21-010':('ins2098256','130817'), 'ATLAS_EXOT-2022-18':('ins2682337','140530'),
 'CMS_EXO-24-039':('ins3205293','169576'), 'CMS_B2G-20-009':('ins2159368','132485'),
 'CMS_EXO-17-021':('ins1685989',None), 'CMS_EXO-19-019':('ins1849964','101186'),
 'CMS_HIG-20-017':('ins1857811','102461'), 'ATLAS_EXOT-2018-32':('ins1782373',None),
 'ATLAS_EXOT-2018-08':('ins1725190',None), 'ATLAS_HDBS-2023-19':('ins2807795',None),
 'ATLAS_EXOT-2022-38':('146753','146753'), 'ATLAS_HIGG-2018-27':('100161','100161'),
 'ATLAS_HDBS-2023-17':('ins2726938',None),'ATLAS_EXOT-2018-49':('ins3094414',None),
 'CMS_EXO-22-024':('ins2787227','150677')}
hepdata=[]
for a,(rid,doi) in primary.items():
    hepdata.append({'analysis':a,'record_id':rid,'record_url':'https://www.hepdata.net/record/'+rid,
      'doi':('10.17182/hepdata.'+doi) if doi else None,
      'yaml_export_url':'https://www.hepdata.net/download/submission/'+rid+'/yaml',
      'priority':'core' if a in ['CMS_EXO-21-010','ATLAS_EXOT-2022-18','CMS_EXO-24-039','CMS_B2G-20-009'] else 'comparison',
      'status':'not downloaded; HEPData endpoint challenge encountered in this environment; record-specific retrievability not assumed',
      'version_policy':'Latest is a moving target. On retrieval save version, DOI, modification timestamp and checksum.'})
write(B/'hepdata_access.json',hepdata)

log=[json.loads(x) for x in (B/'download_log.jsonl').read_text().splitlines()]
latest={}
for r in log:latest[r['path']]=r
pending=[r for p,r in latest.items() if r['status']=='failed' and not (B/p).exists()]
write(B/'pending_public_downloads.json',pending)
summary={
 'snapshot_date':'2026-10-29 UTC (collection directory dated 2026-10-28)',
 'paper_pdfs':len(list((B/'papers').glob('*.pdf'))),
 'result_figure_pdfs':len(list((B/'analyses').rglob('*.pdf'))),
 'result_page_directories':len([d for d in (B/'analyses').iterdir() if d.is_dir()]),
 'opendata_records':len(out),'enumerated_event_files':sum(r['enumerated_root_files'] for r in out),
 'sample_files':len(brief),'sample_bytes':sum(r['bytes'] for r in brief),'sample_events':sum(r['entries'] for r in brief),
 'public_repo_root_files':len(json.loads((B/'code/CMSAnalysis_root_inventory.json').read_text())),
 'exported_repo_histograms':len(json.loads((B/'numerical/cms_public_repo_histograms.json').read_text())),
 'secondary_spectrum_bins':44,'hepdata_records_mapped':len(hepdata),'pending_public_files':len(pending)}
write(B/'collection_summary.json',summary)
print(json.dumps(summary,indent=2))
print('MANIFEST_DISCREPANCIES',[(r['record_id'],r['issues']) for r in out if r['issues']])
