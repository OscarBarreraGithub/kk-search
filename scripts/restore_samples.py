#!/usr/bin/env python3
"""Restore the exact four tested public CERN files. Dry-run unless --execute."""
import argparse,hashlib,json,pathlib,shutil,urllib.parse,urllib.request,zlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
def checked(path,row,sha):
    if not path.is_file() or path.stat().st_size!=row['bytes']:return False
    h=hashlib.sha256();adler=1
    with path.open('rb') as f:
        for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b);adler=zlib.adler32(b,adler)
    return h.hexdigest()==sha and 'adler32:'+format(adler&0xffffffff,'08x')==row['checksum_expected']
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--execute',action='store_true')
    p.add_argument('--source-dir',type=pathlib.Path,help='Reuse existing verified sample files instead of downloading')
    a=p.parse_args();base=ROOT/'kk_data_access_2026-10-28'
    if not (base/'SHA256.json').exists():p.error('Run scripts/materialize.py first')
    samples=json.loads((ROOT/'inventory/validated_samples.json').read_text())
    sha={r['path']:r['sha256'] for r in json.loads((ROOT/'inventory/SHA256.json').read_text())}
    print(json.dumps({'files':len(samples),'bytes':sum(r['bytes'] for r in samples),'execute':a.execute}),flush=True)
    if not a.execute:return
    failures=[]
    for r in samples:
        dest=base/r['file'];expected=sha[r['file']]
        if checked(dest,r,expected):print('Verified existing:',dest.name,flush=True);continue
        dest.parent.mkdir(parents=True,exist_ok=True);partial=dest.with_name(dest.name+'.partial')
        try:
            if a.source_dir:
                src=a.source_dir/dest.name
                if not checked(src,r,expected):raise ValueError('Existing source sample does not match manifest')
                shutil.copyfile(src,partial)
            else:
                url=r['https_url'];u=urllib.parse.urlparse(url)
                if u.scheme!='https' or u.hostname!='opendata.cern.ch':raise ValueError('Unexpected source domain')
                req=urllib.request.Request(url,headers={'User-Agent':'KKSearchPublicData/1.0'})
                with urllib.request.urlopen(req,timeout=120) as src,partial.open('wb') as out:
                    n=0
                    while b:=src.read(4*1024*1024):
                        n+=len(b)
                        if n>r['bytes']:raise ValueError('Download exceeds expected size')
                        out.write(b)
            if not checked(partial,r,expected):raise ValueError('Size or checksum mismatch')
            partial.replace(dest);print('Restored and verified:',dest.name,flush=True)
        except Exception as e:failures.append({'file':r['file'],'error':str(e)})
    if failures:print(json.dumps(failures,indent=2));raise SystemExit(1)
if __name__=='__main__':main()
