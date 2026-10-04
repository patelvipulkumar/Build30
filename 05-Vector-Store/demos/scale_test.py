import time
import numpy as np
D = 384
rng = np.random.default_rng(7)
query = rng.standard_normal(D).astype(np.float32)
query /= np.linalg.norm(query)
for n in (1_000, 10_000, 100_000, 200_000):
    matrix = rng.standard_normal((n, D)).astype(np.float32)
    matrix /= np.linalg.norm(matrix, axis=1, keepdims=True)
    start = time.perf_counter()
    scores = matrix @ query
    top = np.argsort(-scores)[:5]
    ms = (time.perf_counter() - start) * 1000
    mb = matrix.nbytes / 1_000_000
    print(f'N={n:>8,}   {ms:8.2f} ms per query   {mb:8.1f} MB in memory')
for n in (1_000_000, 10_000_000):
    gb = n * D * 4 / 1_000_000_000
    print(f'N={n:>10,}   would need {gb:6.2f} GB just for float32 vectors')