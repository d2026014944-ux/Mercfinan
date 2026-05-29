from fastapi.testclient import TestClient

from apps.api.main import app
from apps.data_worker.main import build_feature_window
from model_core.input_schema import MODEL_INPUT_SIZE


def test_data_worker_payload_reaches_api() -> None:
    closes = [100.0 + index for index in range(MODEL_INPUT_SIZE + 2)]
    payload = build_feature_window(closes, MODEL_INPUT_SIZE)

    client = TestClient(app)
    response = client.post("/predict", json={"values": payload})

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body["prediction"], float)
