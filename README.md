# Movie Recommendation System

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=flat-square&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red?style=flat-square&logo=streamlit)
![Dataset](https://img.shields.io/badge/Dataset-MovieLens%20100K-lightgrey?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

End-to-end content-based and item-item collaborative filtering movie recommender built on the MovieLens 100K dataset. Provides a FastAPI backend with a `/recommend` endpoint and an interactive Streamlit dashboard for personalized recommendations.

---

## Business Problem

Streaming platforms lose engagement when users cannot discover relevant content. This system identifies movies similar to what a user already enjoys — the same algorithm powering Netflix and Spotify recommendations — demonstrating cosine similarity-based collaborative filtering at scale.

---

## Features

- Load MovieLens data and build a user-movie interaction matrix
- Compute movie-movie cosine similarity, cached to disk
- REST API: top-N similar movies for a list of liked movie IDs
- Streamlit UI: interactive selection and recommendation visualization
- Reproducible scripts: build similarity matrix once, serve instantly

---

## Project Structure

```
movie-recommender/
├── api/
│   └── main.py                  # FastAPI app (/ and /recommend)
├── app/
│   └── streamlit_app.py         # Streamlit dashboard
├── data/
│   └── ml-100k/                 # MovieLens files (u.item, u.data)
├── models/
│   └── movie_similarity.npz     # Precomputed similarity matrix
├── scripts/
│   └── build_similarity.py      # Build & cache similarity matrix
├── utils/
│   ├── data.py                  # Load and clean data
│   └── recommender.py           # Core recommend() logic
├── requirements.txt
└── README.md
```

---

## Quickstart

```bash
# 1. Clone & setup
git clone https://github.com/deepanshu0110/movie-recommender.git
cd movie-recommender
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate     # Windows
pip install -r requirements.txt

# 2. Download MovieLens 100K from https://grouplens.org/datasets/movielens/100k/
# Extract to data/ml-100k/ (u.data and u.item must exist)

# 3. Build similarity matrix (one-time)
python scripts/build_similarity.py \
  --data_dir data/ml-100k \
  --out models/movie_similarity.npz

# 4. Start API (Terminal 1)
uvicorn api.main:app --reload --port 8000

# 5. Start Dashboard (Terminal 2)
streamlit run app/streamlit_app.py
```

---

## API Usage

```bash
# Get top 5 movies similar to movie IDs 1, 50, 100
curl -X POST http://localhost:8000/recommend \
  -H 'Content-Type: application/json' \
  -d '{"movie_ids": [1, 50, 100], "top_n": 5}'
```

---

## Access

| Service | URL |
|---|---|
| API Root | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| Dashboard | http://localhost:8501 |

---

## Tech Stack

Python · Pandas · NumPy · Scikit-learn (cosine similarity) · FastAPI · Streamlit · SciPy

---

## License

MIT License