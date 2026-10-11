"""Shallow autoencoder baseline (d -> 8 -> d), reconstruction MSE as the anomaly score."""

from __future__ import annotations

from collections import deque
from typing import Sequence

import numpy as np
import torch
from torch import nn

from rad.models.base import FixedMinMaxScaler, squash_array


class AutoencoderDetector:
    """Features are min-max scaled with bootstrap-frozen bounds; the net trains by replay.

    `bootstrap` takes `bootstrap_steps` Adam steps on seeded minibatches of the
    bootstrap data. Each later `learn_one` adds the window to a bounded replay
    buffer and takes `steps_per_learn` steps on minibatches drawn from it.
    Score = squash(MSE).
    """

    def __init__(self, features: Sequence[str], hidden: int = 8, lr: float = 1e-2, bootstrap_steps: int = 1000,
                 steps_per_learn: int = 20, batch_size: int = 32, buffer: int = 2880, margin: float = 0.25,
                 seed: int = 0) -> None:
        self.features = tuple(features)
        self.scaler = FixedMinMaxScaler(self.features, margin=margin)
        self.bootstrap_steps = bootstrap_steps
        self.steps_per_learn = steps_per_learn
        self.batch_size = batch_size
        self.buffer: deque[np.ndarray] = deque(maxlen=buffer)
        self.rng = np.random.default_rng(seed)
        torch.manual_seed(seed)
        d = len(self.features)
        self.net = nn.Sequential(nn.Linear(d, hidden), nn.ReLU(), nn.Linear(hidden, d), nn.Sigmoid())
        self.opt = torch.optim.Adam(self.net.parameters(), lr=lr)
        self.loss = nn.MSELoss()

    def _train(self, data: np.ndarray, steps: int) -> None:
        tensor = torch.as_tensor(data, dtype=torch.float32)
        for _ in range(steps):
            idx = torch.as_tensor(self.rng.integers(0, len(data), size=min(self.batch_size, len(data))))
            batch = tensor[idx]
            self.opt.zero_grad()
            loss = self.loss(self.net(batch), batch)
            loss.backward()
            self.opt.step()

    def bootstrap(self, xs: Sequence[dict[str, float]]) -> None:
        self.scaler.fit(xs)
        for x in xs:
            self.buffer.append(self.scaler.transform_vec(x))
        self._train(self.scaler.matrix_scaled(xs), self.bootstrap_steps)

    def score_many(self, xs: Sequence[dict[str, float]]) -> np.ndarray:
        v = torch.as_tensor(self.scaler.matrix_scaled(xs), dtype=torch.float32)
        with torch.no_grad():
            mse = ((self.net(v) - v) ** 2).mean(dim=1).numpy()
        return squash_array(mse)

    def score_one(self, x: dict[str, float]) -> float:
        return float(self.score_many([x])[0])

    def learn_one(self, x: dict[str, float]) -> None:
        self.buffer.append(self.scaler.transform_vec(x))
        self._train(np.vstack(self.buffer), self.steps_per_learn)

    def model_bytes(self) -> int:
        """float32 weights and biases plus the frozen scaler bounds (D26); the replay buffer is not counted."""
        return 4 * sum(p.numel() for p in self.net.parameters()) + 2 * 4 * len(self.features)
