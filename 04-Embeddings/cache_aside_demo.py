from cache_aside import cache_aside
@cache_aside('demo-model', 'cache/demo_cache.json')
def slow_embed(text):
    print('computing for:', text)
    return [len(text), text.count('a')]
print(slow_embed('banana'))
print(slow_embed('banana'))
print(slow_embed('apple'))
print('hits', slow_embed.hits, 'misses', slow_embed.misses)