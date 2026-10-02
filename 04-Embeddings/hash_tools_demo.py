from pathlib import Path
from hash_tools import find_changed, group_duplicates
docs = Path('docs')
docs.mkdir(exist_ok=True)
(docs / 'a.txt').write_text('first file')
(docs / 'b.txt').write_text('second file')
paths = sorted(docs.glob('*.txt'))
print('run 1 changed:', find_changed(paths, 'cache/manifest.json'))
print('run 2 changed:', find_changed(paths, 'cache/manifest.json'))
(docs / 'b.txt').write_text('second file edited')
print('run 3 changed:', find_changed(paths, 'cache/manifest.json'))
print(group_duplicates(['Hello world', 'hello   world', 'bye', 'Bye', 'other']))