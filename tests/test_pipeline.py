import sys

from tests.helpers import ROOT, run_script


def test_download_train_and_recommend():
    run_script("download_data.py")
    output = run_script("train_model.py")
    assert "recommendations" in output.lower()

    from fastapi.testclient import TestClient

    sys.path.insert(0, str(ROOT))
    from api.app import app

    with TestClient(app) as client:
        response = client.post("/recommend?n_recommendations=5", json=[1, 50, 100])
        assert response.status_code == 200
        recs = response.json()["recommendations"]
        assert len(recs) == 5
        assert all(r["movie_id"] not in (1, 50, 100) for r in recs)
