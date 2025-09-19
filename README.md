# 🎬 Movie Recommendation System

A simple end‑to‑end **content‑based / item–item collaborative** movie recommender built on the MovieLens dataset.  
It provides:
- a **FastAPI** backend with a `/recommend` endpoint, and
- a **Streamlit** dashboard where users pick favorite movies and see personalized recommendations.

The screenshots below show the API root (`localhost:8000`) and the Streamlit UI (`localhost:8501`).

---

## ✨ Features
- Load MovieLens data and build a **user–movie interaction matrix**.
- Compute **movie–movie cosine similarity** and cache it to `models/`.
- REST API to return **top‑N similar movies** for a list of liked movie IDs.
- Streamlit app for interactive selection and visualization of recommendations.
- Clean project layout and reproducible scripts.

---

## 🧱 Project Structure
```
movie-recommender/
├─ api/
│  └─ main.py                  # FastAPI app (endpoints: / and /recommend)
├─ app/
│  └─ streamlit_app.py         # Streamlit dashboard
├─ data/
│  └─ ml-100k/                 # MovieLens data (u.item, u.data, etc.)
├─ models/
│  └─ movie_similarity.npz     # Precomputed cosine-similarity matrix
├─ scripts/
│  └─ build_similarity.py      # Build & save the similarity matrix
├─ utils/
│  ├─ data.py                  # Load/clean data
│  └─ recommender.py           # Core recommend() logic
├─ requirements.txt
└─ README.md
```
> Tip: keep large artifacts (`data/`, `models/`) out of Git. Use `.gitignore` or Git LFS.

---

## 📦 Setup

### 1) Create and activate a virtual environment
```bash
# Windows (PowerShell)
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1

# macOS/Linux
python -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

### 3) Download MovieLens (100k)
Download **MovieLens 100k** from GroupLens and extract into `data/ml-100k/` so that files like `u.data`, `u.item` exist at:
```
data/ml-100k/u.data
data/ml-100k/u.item
```

### 4) Build the similarity matrix
```bash
python scripts/build_similarity.py \
  --data_dir data/ml-100k \
  --out models/movie_similarity.npz
```
This script:
- Loads movies & ratings, builds a **user–movie matrix** (rows = users, cols = movies).
- Computes **cosine similarity** between movie vectors.
- Saves a sparse array to `models/movie_similarity.npz` and a mapping of `movieId -> col index` (usually as `models/index.json`).

---

## 🚀 Run the services

### Backend API (FastAPI + Uvicorn)
```bash
uvicorn api.main:app --reload --port 8000
```
Now open http://localhost:8000 — you should see:
```json
{"message":"Movie Recommendation API"}
```
Interactive docs: http://localhost:8000/docs

#### `/recommend` (POST)
**Request body**
```json
{
  "liked_movie_ids": [50, 172, 181],
  "top_n": 10
}
```
**Response** (example)
```json
{
  "recommendations": [
    {"movie_id": 96, "title": "Terminator 2: Judgment Day (1991)", "similarity": 0.321},
    {"movie_id": 89, "title": "Blade Runner (1982)", "similarity": 0.313}
  ]
}
```

### Frontend (Streamlit)
```bash
streamlit run app/streamlit_app.py --server.port 8501
```
Open http://localhost:8501 and select your favorite movies, set **N**, and click **Get Recommendations**.

---

## 🧪 Quick tests

**cURL**
```bash
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d "{\"liked_movie_ids\":[50,172,181],\"top_n\":5}"
```

**Python**
```python
import requests
r = requests.post("http://localhost:8000/recommend",
                  json={"liked_movie_ids":[50,172,181], "top_n":5})
print(r.json())
```

---

## ⚙️ How it works (short version)
1. **Matrix build**: Construct a dense/sparse matrix `R` of shape `(n_users, n_movies)` from `u.data` ratings.
2. **Item–item similarity**: Compute cosine similarity across **columns** of `R` → `S = cosine_similarity(R.T)`.
3. **Scoring**: Given liked movies `L`, score each candidate movie `m` as the weighted sum of similarities to `L`.
4. **Filter & rank**: Exclude already‑liked movies and return top‑N by score.

You can switch to a TF‑IDF-of‑genres model or hybrid easily by editing `utils/recommender.py`.

---

## 🗂️ Environment & config
- Python ≥ 3.9
- `requirements.txt` includes: `fastapi`, `uvicorn`, `pandas`, `numpy`, `scipy`, `scikit-learn`, `streamlit`, `pydantic`.

If you store paths in a `.env`, load them in `api/main.py` and `app/streamlit_app.py` with `python-dotenv`.

---

## ☁️ Deploying the code to **GitHub**

### A. One-time Git setup
```bash
git init
git branch -M main

# Good .gitignore (see below)
echo "" >> .gitignore

git add .
git commit -m "Initial commit: Movie Recommendation System"
```

### B. Create a GitHub repo
1. Go to GitHub → **New repository** → name it `movie-recommender`.
2. Copy the **remote URL** (HTTPS).

### C. Connect and push
```bash
git remote add origin https://github.com/<your-username>/movie-recommender.git
git push -u origin main
```

> **Do NOT push** the full `data/` or `models/` folders. They are large and unnecessary for source control.  
> If you need to share artifacts, consider **Git LFS** or publish a small sample plus a build script.

### Suggested `.gitignore`
```
# Python
.venv/
__pycache__/
*.pyc
*.pyo
*.pyd
*.egg-info/

# Data / Models
data/
models/
!data/.gitkeep
!models/.gitkeep

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

Create empty keep files if you want folders to exist without contents:
```bash
mkdir -p data models
echo > data/.gitkeep
echo > models/.gitkeep
```

---

## 📦 Optional: Docker (local)
```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```
Build & run:
```bash
docker build -t movie-rec .
docker run -p 8000:8000 movie-rec
```

---

## 🔧 Troubleshooting
- **KeyError: movieId not found** → Ensure your movie ID mapping aligns between `models/index.json` and `app/api`.
- **Matrix memory error** → Use `scipy.sparse` and chunked cosine similarity or reduce to popular movies.
- **CORS from Streamlit to API** → Enable CORSMiddleware in `api/main.py`.
- **Port already in use** → Change with `--port 8001` (API) / `--server.port 8502` (Streamlit).

---

## 📄 License
MIT (feel free to adapt for learning and demos)
