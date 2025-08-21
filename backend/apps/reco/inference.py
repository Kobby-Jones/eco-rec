import json, numpy as np
from django.db import connection
from apps.catalog.models import Product
from .ann_index import query_index


WEIGHTS = {"view":0.2,"click":0.5,"add_to_cart":0.8,"purchase":1.0,"rating":1.0}


def compute_user_vector(user_id:int, recent_k:int=50):
    with connection.cursor() as cur:
        cur.execute("""
        SELECT product_id, type FROM interactions_interaction
        WHERE user_id=%s ORDER BY ts DESC LIMIT %s
        """, [user_id, recent_k])
        rows = cur.fetchall()
    if not rows:
        return None
    vecs, wts = [], []
    with connection.cursor() as cur:
        for pid, t in rows:
            cur.execute("SELECT vector FROM reco_productembedding WHERE product_id=%s", [pid])
            r = cur.fetchone()
            if r:
                v = np.array(json.loads(r[0]), dtype=np.float32)
                vecs.append(v); wts.append(WEIGHTS.get(t,0.3))
    if not vecs:
        return None
    W = np.array(wts, dtype=np.float32)[:,None]
    V = np.vstack(vecs)
    return ((W*V).sum(axis=0) / (W.sum()+1e-6)).astype(np.float32)


def business_rules(products):
    return [p for p in products if p.is_active]


def recommend_for_user(user_id:int, k:int=20):
    v = compute_user_vector(user_id)
    if v is None:
        qs = Product.objects.filter(is_active=True).order_by("-id")[:k]
        return [(p, 0.0) for p in qs]
    ids, scores = query_index(v, k=200)
    qs = list(Product.objects.filter(id__in=ids, is_active=True))
    id2p = {p.id:p for p in qs}
    ranked = [(id2p[i], float(s)) for i,s in zip(ids, scores) if i in id2p]
    ranked_products = business_rules([p for p,_ in ranked])
    return [(p, 1.0) for p in ranked_products[:k]]