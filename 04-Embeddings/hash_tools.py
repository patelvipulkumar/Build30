import hashlib
import json
from pathlib import Path
def file_hash(path):
    sha = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(65536), b''):
            sha.update(block)
    return sha.hexdigest()
def find_changed(paths, manifest_path):
    manifest_file = Path(manifest_path)
    old = json.loads(manifest_file.read_text(encoding='utf-8')) if manifest_file.exists() else {}
    new = {}
    changed = []
    for path in paths:
        digest = file_hash(path)
        new[str(path)] = digest
        if old.get(str(path)) != digest:
            changed.append(str(path))
    manifest_file.parent.mkdir(parents=True, exist_ok=True)
    manifest_file.write_text(json.dumps(new), encoding='utf-8')
    return changed
def group_duplicates(texts):
    groups = {}
    for index, text in enumerate(texts):
        key = hashlib.sha256(' '.join(text.split()).lower().encode('utf-8')).hexdigest()
        groups.setdefault(key, []).append(index)
    return [indexes for indexes in groups.values() if len(indexes) > 1]