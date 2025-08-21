# GNN Recommender — Django + React + PyTorch Geometric


## Prereqs
- Docker & Docker Compose (recommended) OR local Python 3.11 + Node 20
- Postgres 16, Redis 7 (Compose spins these up for you)


## Quick start (Docker)
```bash
cp .env.example .env
docker compose up --build -d db redis
docker compose up --build backend worker frontend
# Wait for backend init, then run migrations:
docker compose exec backend bash -lc "python manage.py migrate && python manage.py createsuperuser --noinput --username admin --email admin@example.com || true"
# Load sample data:
docker compose exec backend python manage.py load_sample
# Train & build ANN index (small demo):
docker compose exec backend python manage.py shell -c "from apps.reco.train import train; train(); from apps.reco.ann_index import build_faiss_index; build_faiss_index()"
# Open frontend at http://localhost:5173

# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp ../.env .env || cp ../.env.example .env
python manage.py migrate
python manage.py runserver 0.0.0.0:8000


# Frontend
cd ../frontend
npm i
npm run dev -- --host

### `.env.example`
```env
# Backend
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=True
DATABASE_URL=postgres://app:app@db:5432/app
REDIS_URL=redis://redis:6379/0
ALLOWED_HOSTS=*
CORS_ALLOWED_ORIGINS=http://localhost:5173
MODEL_DIR=/models


# Frontend
VITE_API_BASE=http://localhost:8000