from __future__ import annotations

import hashlib
import logging
import os
from pathlib import Path
from urllib.request import urlopen

import torch

from model_core.input_schema import ensure_window_size
from model_core.model import create_model
from model_core.preprocessing import normalize_window

logger = logging.getLogger(__name__)


class InferenceService:
    def __init__(self) -> None:
        self._model = create_model()
        self._load_weights_if_available()

    def _load_weights_if_available(self) -> None:
        model_path = Path(os.getenv("MODEL_PATH", "/app/models/model.pt"))
        if not model_path.exists():
            if self._try_download_model(model_path):
                logger.info("Model downloaded to %s", model_path)
            else:
                logger.warning("Model weights not found at %s; using default weights", model_path)
                return

        artifact = torch.load(model_path, map_location="cpu")
        if isinstance(artifact, torch.nn.Module):
            self._model = artifact
        else:
            state_dict = artifact["state_dict"] if isinstance(artifact, dict) and "state_dict" in artifact else artifact
            if not isinstance(state_dict, dict):
                raise ValueError("Unsupported model artifact format")
            self._model.load_state_dict(state_dict)

        self._model.eval()

    def _try_download_model(self, model_path: Path) -> bool:
        download_url = os.getenv("MODEL_DOWNLOAD_URL")
        if not download_url:
            return False

        model_path.parent.mkdir(parents=True, exist_ok=True)
        with urlopen(download_url) as response:  # nosec B310 - URL is controlled by deployment config
            data = response.read()
        model_path.write_bytes(data)

        expected_hash = os.getenv("MODEL_SHA256")
        if expected_hash:
            actual_hash = hashlib.sha256(data).hexdigest()
            if actual_hash != expected_hash:
                model_path.unlink(missing_ok=True)
                raise ValueError("Downloaded model hash mismatch")

        return True

    def predict(self, values: list[float]) -> float:
        ensure_window_size(values)
        normalized = normalize_window(values)
        features = torch.tensor(normalized, dtype=torch.float32).unsqueeze(0)
        with torch.no_grad():
            prediction = self._model(features)
        return float(prediction.squeeze().item())
