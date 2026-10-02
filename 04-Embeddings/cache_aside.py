import functools
import hashlib
import json
from pathlib import Path
def cache_aside(model_name, path):
    file = Path(path)
    store = json.loads(file.read_text(encoding='utf-8')) if file.exists() else {}
    def decorator(func):
        @functools.wraps(func)
        def wrapper(text):
            key = hashlib.sha256((model_name + '||' + text).encode('utf-8')).hexdigest()
            if key in store:
                wrapper.hits += 1
                return store[key]
            wrapper.misses += 1
            value = func(text)
            store[key] = value
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text(json.dumps(store), encoding='utf-8')
            return value
        wrapper.hits = 0
        wrapper.misses = 0
        return wrapper
    return decorator