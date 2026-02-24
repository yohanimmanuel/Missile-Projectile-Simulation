"""
Simulation-only moving target in 3D.
Supports configurable velocity patterns in abstract 3D space.
No real-world targeting or military parameters.
"""

import math
import random
from typing import Literal

from Vector3D import Vector3D
from config import (
    TARGET_LINEAR_SPEED,
    TARGET_RANDOM_SEED,
    TARGET_WOBBLE_AMPLITUDE,
    TARGET_WOBBLE_FREQUENCY,
    TARGET_JITTER,
)

MovementMode3D = Literal["linear", "sinusoidal", "random"]
ModeSchedule = Literal["fixed", "random_switch"]


class Target3D:
    """
    Simulates a moving object in 3D with configurable velocity patterns.
    Simulation only - fictional behavior for pursuit demo.
    """

    def __init__(
        self,
        position: Vector3D,
        mode: MovementMode3D = "linear",
        linear_direction: Vector3D | None = None,
        mode_schedule: ModeSchedule = "fixed",
    ) -> None:
        """
        Args:
            position: Initial position in abstract 3D space.
            mode: Initial mode: 'linear', 'sinusoidal', or 'random'.
            linear_direction: For 'linear' mode, unit direction vector. If None, uses (1,0,0).
            mode_schedule: 'fixed' = use mode for whole run; 'random_switch' = randomly change mode during run.
        """
        self.position = position.copy()
        self.mode = mode
        self.mode_schedule = mode_schedule
        self._linear_direction = (
            linear_direction.normalized()
            if linear_direction is not None and linear_direction.magnitude() > 1e-10
            else Vector3D(1.0, 0.0, 0.0)
        )
        self._time: float = 0.0
        self._next_mode_switch_time: float = 0.0
        if TARGET_RANDOM_SEED is not None:
            random.seed(TARGET_RANDOM_SEED)

    def update(self, dt: float) -> None:
        """
        Advance target position by one timestep. Fighter-jet style: curved, random-looking path.
        Simulation only.
        """
        self._time += dt
        self._apply_jitter()
        velocity = self._compute_velocity()
        self.position = self.position + velocity * dt

    def _perp_unit_1(self) -> Vector3D:
        """A unit vector perpendicular to _linear_direction (for wobble)."""
        d = self._linear_direction
        if abs(d.y) < 1e-10 and abs(d.z) < 1e-10:
            return Vector3D(0.0, 1.0, 0.0)
        return Vector3D(0.0, -d.z, d.y).normalized()

    def _perp_unit_2(self) -> Vector3D:
        """Another unit vector perpendicular to _linear_direction and _perp_unit_1."""
        return self._linear_direction.cross(self._perp_unit_1()).normalized()

    def _apply_jitter(self) -> None:
        """Small random heading change so path is irregular, not a perfect curve. Simulation only."""
        j = TARGET_JITTER
        dx = random.uniform(-j, j)
        dy = random.uniform(-j, j)
        dz = random.uniform(-j, j)
        self._linear_direction = (
            self._linear_direction + Vector3D(dx, dy, dz)
        ).normalized()

    def _compute_velocity(self) -> Vector3D:
        """
        Target flies toward current direction with perpendicular wobble — curved, free-way motion
        like a fighter jet, not a straight line. Still progresses across the sky via waypoints.
        """
        main = self._linear_direction * TARGET_LINEAR_SPEED
        t = self._time * TARGET_WOBBLE_FREQUENCY
        p1 = self._perp_unit_1()
        p2 = self._perp_unit_2()
        wobble = (math.sin(t) * p1 + math.cos(t * 1.3) * p2) * TARGET_WOBBLE_AMPLITUDE
        return main + wobble

    def set_random_direction(self) -> None:
        """
        Set _linear_direction to a new random 3D unit vector.
        So the target changes heading, not just motion style. Simulation only.
        """
        theta = random.uniform(0, 2 * math.pi)
        phi = math.acos(random.uniform(-1, 1))
        self._linear_direction = Vector3D(
            math.sin(phi) * math.cos(theta),
            math.sin(phi) * math.sin(theta),
            math.cos(phi),
        )

    def set_direction_toward(self, point: Vector3D) -> None:
        """
        Set _linear_direction to point from current position toward the given point.
        Use so the target flies across the space toward waypoints, not swirling in place.
        Simulation only.
        """
        delta = point - self.position
        if delta.magnitude() < 1e-10:
            self.set_random_direction()
            return
        self._linear_direction = delta.normalized()

    def get_position(self) -> Vector3D:
        """Return current position (copy)."""
        return self.position.copy()
