from config import DATA_DIR
from dedupe import keep_first, near_duplicates_fast
from embedder import Embedder
from main import load_sentences
rows = load_sentences(DATA_DIR / 'sentences.txt')
texts = [row[1] for row in rows]
texts += ['A kitten plays with a toy.', 'The server went down after we deployed.', 'Boil pasta for 10 minutes.']
vectors = Embedder('minilm').embed_documents(texts)
threshold = 0.85
for i, j, score in near_duplicates_fast(vectors, threshold):
    print(f'{score:.3f}')
    print('   ' + texts[i])
    print('   ' + texts[j])
kept = keep_first(vectors, threshold)
print(f'kept {len(kept)} of {len(texts)}')