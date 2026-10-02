import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from config import BASE_DIR, DATA_DIR, DEFAULT_MODEL
from embedder import Embedder
from main import load_sentences
rows = load_sentences(DATA_DIR / 'sentences.txt')
topics = [row[0] for row in rows]
texts = [row[1] for row in rows]
vectors = Embedder(DEFAULT_MODEL).embed_documents(texts)
points = PCA(n_components=2).fit_transform(vectors)
colors = {'cats': 'tab:orange', 'dogs': 'tab:brown', 'money': 'tab:green', 'cooking': 'tab:red', 'tech': 'tab:blue'}
plt.figure(figsize=(9, 6))
for topic in colors:
    chosen = [i for i, t in enumerate(topics) if t == topic]
    plt.scatter(points[chosen, 0], points[chosen, 1], label=topic, c=colors[topic], s=90)
for i, text in enumerate(texts):
    plt.annotate(text[:22], (points[i, 0], points[i, 1]), fontsize=7)
plt.legend()
plt.title('384 dimensions squeezed into 2')
plt.savefig(BASE_DIR / 'plot.png', dpi=150, bbox_inches='tight')
print('saved plot.png')