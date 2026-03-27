# Movie Recommendation System

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=flat-square&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red?style=flat-square&logo=streamlit)
![Dataset](https://img.shields.io/badge/Dataset-MovieLens%20100K-lightgrey?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

Item-item collaborative filtering recommender on MovieLens 100K. Precomputes cosine similarity, serves a `/recommend` API, and provides an interactive Streamlit UI.

---

## Business Problem

Streaming platforms lose watch-time when users can't find their next film. This system identifies movies similar to what a user already rated — the same pattern behind Netflix and Spotify recommendations.

---

## Quickstart

```bash
git clone https://github.com/deepanshu0110/movie-recommender.git
cd movie-recommender
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# Download MovieLens 100K, extract u.data + u.item to data/ml-100k/
python scripts/build_similarity.py --data_dir data/ml-100k --out models/movie_similarity.npz
uvicorn api.main:app --reload --port 8000   # Terminal 1
streamlit run app/streamlit_app.py           # Terminal 2
```

## API Usage

```bash
curl -X POST http://localhost:8000/recommend -H 'Content-Type: application/json' -d '{"movie_ids": [1, 50, 100], "top_n": 5}'
```

---

## Tech Stack

Python · Pandas · NumPy · Scikit-learn · SciPy · FastAPI · Streamlit

---

## Author

**Deepanshu Garg** — Freelance Data Scientist
- GitHub: [@deepanshu0110](https://github.com/deepanshu0110)
- Hire: [freelancer.com/u/deepanshu0110](https://www.freelancer.com/u/deepanshu0110)

MIT License