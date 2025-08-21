from config.celery import app


@app.task
def train_gnn_task():
    from .train import train
    return train()


@app.task
def refresh_ann_task():
    from .ann_index import build_faiss_index
    build_faiss_index()