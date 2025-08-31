import os, json, random
import numpy as np, pandas as pd, torch
from torch_geometric.data import HeteroData
from django.db import connection
from .model_gnn import HeteroLP

EMB_DIM = 64
BATCH = 4096
EPOCHS = 10
MODEL_PATH = "/models/gnn_model.pt"

def fetch_edges():
    with connection.cursor() as cur:
        cur.execute("""
        SELECT user_id, product_id, type, COALESCE(value,1.0) as w
        FROM interactions_interaction
        """)
        rows = cur.fetchall()
    return pd.DataFrame(rows, columns=["user_id","product_id","type","w"])

def fetch_products():
    with connection.cursor() as cur:
        cur.execute("SELECT id, category_id, COALESCE(brand,'') FROM catalog_product WHERE is_active=true")
        rows = cur.fetchall()
    return pd.DataFrame(rows, columns=["product_id","category_id","brand"])

def build_graph():
    inter = fetch_edges()
    prods = fetch_products()

    # Force Python ints in the ID maps
    u_ids = {int(u): i for i, u in enumerate(inter["user_id"].unique())}
    p_ids = {int(p): i for i, p in enumerate(prods["product_id"].unique())}
    c_ids = {int(c): i for i, c in enumerate(prods["category_id"].dropna().unique())}
    b_ids = {str(b): i for i, b in enumerate(prods["brand"].astype(str).unique())}

    data = HeteroData()
    data["user"].num_nodes = len(u_ids)
    data["product"].num_nodes = len(p_ids)
    data["category"].num_nodes = len(c_ids)
    data["brand"].num_nodes = len(b_ids)

    # Init embeddings
    for n in ["user", "product", "category", "brand"]:
        data[n].x = torch.nn.Embedding(getattr(data[n], "num_nodes"), EMB_DIM).weight

    # --- User -> Product edges (and reverse)
    for t in ["view", "click", "add_to_cart", "purchase", "rating"]:
        e = inter[inter["type"] == t]
        if len(e) == 0:
            continue

        src = torch.tensor([u_ids[int(u)] for u in e["user_id"].values], dtype=torch.long)
        dst = torch.tensor([p_ids[int(p)] for p in e["product_id"].values], dtype=torch.long)

        data["user", t, "product"].edge_index = torch.stack([src, dst], dim=0)
        data["product", f"rev_{t}", "user"].edge_index = torch.stack([dst, src], dim=0)

    # --- Product -> Category edges (and reverse)
    pc = prods.dropna(subset=["category_id"])
    if len(pc):
        src = torch.tensor([p_ids[int(p)] for p in pc["product_id"].values], dtype=torch.long)
        dst = torch.tensor([c_ids[int(c)] for c in pc["category_id"].values], dtype=torch.long)
        data["product", "belongs_to", "category"].edge_index = torch.stack([src, dst], dim=0)
        data["category", "rev_belongs_to", "product"].edge_index = torch.stack([dst, src], dim=0)

    # --- Product -> Brand edges (and reverse)
    pb = prods
    if len(pb):
        src = torch.tensor([p_ids[int(p)] for p in pb["product_id"].values], dtype=torch.long)
        dst = torch.tensor([b_ids[str(b)] for b in pb["brand"].astype(str).values], dtype=torch.long)
        data["product", "belongs_to", "brand"].edge_index = torch.stack([src, dst], dim=0)
        data["brand", "rev_belongs_to", "product"].edge_index = torch.stack([dst, src], dim=0)

    meta = data.metadata()
    return data, meta, u_ids, p_ids



def build_training_pairs(inter, u_ids, p_ids):
    pos = inter[inter["type"].isin(["click","add_to_cart","purchase"])]
    pos = pos[ pos["user_id"].isin(u_ids) & pos["product_id"].isin(p_ids) ]
    pos_u = torch.tensor([u_ids[u] for u in pos["user_id"].values], dtype=torch.long)
    pos_p = torch.tensor([p_ids[p] for p in pos["product_id"].values], dtype=torch.long)
    U = list(u_ids.values()); P = list(p_ids.values())
    neg_u = torch.tensor(random.choices(U, k=len(pos_u)), dtype=torch.long)
    neg_p = torch.tensor(random.choices(P, k=len(pos_p)), dtype=torch.long)
    return (pos_u, pos_p), (neg_u, neg_p)

def train():
    inter = fetch_edges()
    data, meta, u_ids, p_ids = build_graph()
    (pos_u, pos_p), (neg_u, neg_p) = build_training_pairs(inter, u_ids, p_ids)


    model = HeteroLP(metadata=meta, hidden_channels=EMB_DIM, out_dim=EMB_DIM)
    opt = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-5)
    bce = torch.nn.BCELoss()

    def batchify(u, p, bs=4096):
        for i in range(0, len(u), bs):
            yield u[i:i+bs], p[i:i+bs]

    for epoch in range(EPOCHS):
        model.train(); losses=[]
        for (u_pos, p_pos), (u_neg, p_neg) in zip(batchify(pos_u,pos_p), batchify(neg_u,neg_p)):
            y_pos = model(data.x_dict, data.edge_index_dict, u_pos, p_pos)
            y_neg = model(data.x_dict, data.edge_index_dict, u_neg, p_neg)
            y = torch.cat([y_pos, y_neg], dim=0)
            t = torch.cat([torch.ones_like(y_pos), torch.zeros_like(y_neg)], dim=0)
            loss = bce(y, t)
            opt.zero_grad(); loss.backward(); opt.step()
            losses.append(loss.item())
        print(f"epoch {epoch} loss {np.mean(losses):.4f}")

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    torch.save({"model": model.state_dict(), "meta": meta}, MODEL_PATH)

    model.eval()
    with torch.no_grad():
        h = model.gnn(data.x_dict, data.edge_index_dict)
    item_emb = h["product"].cpu().numpy().astype("float32")

    with connection.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS reco_productembedding (
        product_id BIGINT PRIMARY KEY REFERENCES catalog_product(id),
        vector JSONB NOT NULL,
        updated_at TIMESTAMPTZ DEFAULT now()
        )
        """)
        for p_orig, p_dense in p_ids.items():
            vec = item_emb[p_dense].tolist()
            cur.execute("""
            INSERT INTO reco_productembedding(product_id, vector, updated_at)
            VALUES (%s, %s::jsonb, now())
            ON CONFLICT (product_id) DO UPDATE SET vector=%s::jsonb, updated_at=now()
            """, [p_orig, json.dumps(vec), json.dumps(vec)])

    return True