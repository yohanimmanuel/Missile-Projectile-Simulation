"""
Simulation-only moving target.
Supports configurable velocity patterns in abstract 2D space.
No real-world targeting or military parameters.
"""

import math
import random
from typing import Literal

from Vector2D import Vector2D
from config import (
    TARGET_LINEAR_SPEED,
    TARGET_RANDOM_SEED,
    TARGET_RANDOM_STEP_SCALE,
    TARGET_SINUSOIDAL_AMPLITUDE,
    TARGET_SINUSOIDAL_FREQUENCY,
)

# Movement mode: linear, sinusoidal, or random (evasive)
MovementMode = Literal["linear", "sinusoidal", "random"]


class Target:
    """
    Simulates a moving object with configurable velocity patterns.
    Simulation only - fictional behavior for pursuit demo.
    """

    def __init__(
        self,
        position: Vector2D,
        mode: MovementMode = "linear",
        linear_direction: float | None = None,
    ) -> None:
        """
        Args:
            position: Initial position in abstract 2D space.
            mode: 'linear', 'sinusoidal', or 'random'.
            linear_direction: For 'linear' mode, heading in radians. If None, uses 0.
        """
        self.position = position.copy()
        self.mode = mode
        self._linear_heading = (
            float(linear_direction) if linear_direction is not None else 0.0
        )
        self._time: float = 0.0
        if TARGET_RANDOM_SEED is not None:
            random.seed(TARGET_RANDOM_SEED)

    def update(self, dt: float) -> None:
        """
        Advance target position by one timestep.
        Simulation only - abstract motion model.
        """
        self._time += dt
        velocity = self._compute_velocity()
        self.position = self.position + velocity * dt

    def _compute_velocity(self) -> Vector2D:
        """Compute velocity vector for current mode and time. Fictional logic."""
        if self.mode == "linear":
            return Vector2D.from_heading(self._linear_heading, TARGET_LINEAR_SPEED)
        if self.mode == "sinusoidal":
            # Perpendicular to base direction oscillates
            base = Vector2D.from_heading(self._linear_heading, TARGET_LINEAR_SPEED)
            perp = Vector2D(
                -math.sin(self._linear_heading),
                math.cos(self._linear_heading),
            )
            osc = math.sin(self._time * TARGET_SINUSOIDAL_FREQUENCY) * (
                TARGET_SINUSOIDAL_AMPLITUDE * TARGET_SINUSOIDAL_FREQUENCY
            )
            return base + perp * osc
        if self.mode == "random":
            # Random walk: small random change to heading each step
            self._linear_heading += random.uniform(
                -TARGET_RANDOM_STEP_SCALE * 0.5, TARGET_RANDOM_STEP_SCALE * 0.5
            )
            return Vector2D.from_heading(
                self._linear_heading, TARGET_LINEAR_SPEED * 0.8
            )
        return Vector2D(0.0, 0.0)

    def get_position(self) -> Vector2D:
        """Return current position (copy)."""
        return self.position.copy()
