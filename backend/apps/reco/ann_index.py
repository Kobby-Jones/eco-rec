import faiss, numpy as np, json, os
from django.db import connection
from django.conf import settings


INDEX_PATH = os.path.join(settings.MODEL_DIR, "items.faiss")
IDS_PATH = os.path.join(settings.MODEL_DIR, "item_ids.npy")
D = 64


def load_item_matrix():
    with connection.cursor() as cur:
        cur.execute("SELECT product_id, vector FROM reco_productembedding")
        rows = cur.fetchall()
    ids = np.array([r[0] for r in rows], dtype=np.int64)
    X = np.array([np.array(json.loads(r[1]), dtype=np.float32) for r in rows], dtype=np.float32)
    return ids, X


def build_faiss_index():
    ids, X = load_item_matrix()
    index = faiss.IndexHNSWFlat(D, 32)
    index.hnsw.efConstruction = 200
    faiss.normalize_L2(X)
    index.add(X)
    os.makedirs(settings.MODEL_DIR, exist_ok=True)
    faiss.write_index(index, INDEX_PATH)
    np.save(IDS_PATH, ids)


_def_index = None
_def_ids = None


def _ensure_loaded():
    global _def_index, _def_ids
    if _def_index is None:
        _def_index = faiss.read_index(INDEX_PATH)
        _def_ids = np.load(IDS_PATH)


def query_index(vec, k=200):
    _ensure_loaded()
    x = np.asarray(vec, dtype=np.float32)[None,:]
    faiss.normalize_L2(x)
    D, I = _def_index.search(x, k)
    return _def_ids[I[0]], 1 - D[0]/2