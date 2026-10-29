#!/usr/bin/env python3
"""Restore all archived research sources from the local Git checkout."""
import hashlib,json,pathlib,tarfile,tempfile

ROOT=pathlib.Path(__file__).resolve().parents[1]
def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for c in iter(lambda:f.read(4*1024*1024),b''):h.update(c)
    return h.hexdigest()
def main():
    manifest=json.loads((ROOT/'archives/manifest.json').read_text())
    expected={r['path']:r for r in json.loads((ROOT/'inventory/SHA256.json').read_text())}
    collection=ROOT/manifest['collection_directory']
    restored=0;reused=0
    with tempfile.TemporaryFile() as joined:
        h=hashlib.sha256();total=0
        for item in manifest['parts']:
            part=ROOT/item['path']
            if not part.resolve().is_relative_to(ROOT):raise ValueError('Unsafe archive part path')
            if part.stat().st_size!=item['bytes'] or digest(part)!=item['sha256']:raise ValueError(f'Invalid archive part: {part.name}')
            with part.open('rb') as f:
                for chunk in iter(lambda:f.read(4*1024*1024),b''):joined.write(chunk);h.update(chunk);total+=len(chunk)
        if total!=manifest['archive_bytes'] or h.hexdigest()!=manifest['archive_sha256']:raise ValueError('Combined archive checksum mismatch')
        joined.seek(0)
        with tarfile.open(fileobj=joined,mode='r:gz') as tar:
            for member in tar:
                rel=pathlib.PurePosixPath(member.name)
                if not member.isfile() or rel.is_absolute() or '..' in rel.parts or rel.parts[0]!=collection.name:raise ValueError('Unsafe archive entry')
                dest=ROOT/str(rel)
                if not dest.resolve().is_relative_to(collection.resolve()):raise ValueError('Unsafe extraction path')
                key=str(pathlib.PurePosixPath(*rel.parts[1:]))
                if key=='SHA256.json':target=ROOT/'inventory/SHA256.json';want={'bytes':target.stat().st_size,'sha256':digest(target)}
                else:
                    if key not in expected:raise ValueError(f'Unexpected archive file: {key}')
                    want=expected[key]
                if member.size!=want['bytes']:raise ValueError(f'Unexpected file size: {key}')
                if dest.exists():
                    if dest.stat().st_size==want['bytes'] and digest(dest)==want['sha256']:reused+=1;continue
                    raise ValueError(f'Refusing to overwrite modified file: {dest}')
                dest.parent.mkdir(parents=True,exist_ok=True)
                temp=dest.with_name(dest.name+'.partial');h=hashlib.sha256()
                with tar.extractfile(member) as src,temp.open('wb') as dst:
                    for chunk in iter(lambda:src.read(4*1024*1024),b''):dst.write(chunk);h.update(chunk)
                if h.hexdigest()!=want['sha256']:temp.unlink();raise ValueError(f'Checksum mismatch: {key}')
                temp.replace(dest);restored+=1
    if restored+reused!=manifest['archived_files']:raise ValueError('Unexpected extracted file count')
    print(json.dumps({'collection':str(collection),'restored':restored,'already_verified':reused,'event_samples_to_restore':len(manifest['excluded_event_files'])},indent=2))
if __name__=='__main__':main()
