"""
Simulation-only pursuer (interceptor) in 3D.
Maintains position, velocity, and direction with limited turn rate and speed.
Uses simple steering logic - no real-world guidance algorithms.
"""

from Vector3D import Vector3D
from config import PURSUER_INITIAL_SPEED, PURSUER_MAX_SPEED, PURSUER_MAX_TURN_RATE


class Missile3D:
    """
    Pursuer in 3D: position, velocity, direction vector with max turn rate and max speed.
    Steering is gradual; no instant rotation or teleportation.
    Simulation only - fictional control logic.
    """

    def __init__(self, position: Vector3D, direction: Vector3D | None = None) -> None:
        """
        Args:
            position: Initial position in abstract 3D space.
            direction: Initial direction (unit vector). If None, uses (1, 0, 0).
        """
        self.position = position.copy()
        self.direction = (
            direction.normalized()
            if direction is not None and direction.magnitude() > 1e-10
            else Vector3D(1.0, 0.0, 0.0)
        )
        self.speed = min(float(PURSUER_INITIAL_SPEED), PURSUER_MAX_SPEED)
        self.velocity = self.direction * self.speed

    def apply_direction_correction(
        self, desired_direction: Vector3D, dt: float
    ) -> None:
        """
        Adjust direction toward desired_direction subject to max turn rate.
        Simulation-only steering; not a real guidance law.
        """
        self.direction = self.direction.rotate_toward(
            desired_direction, PURSUER_MAX_TURN_RATE
        )

    def set_speed(self, speed: float) -> None:
        """Clamp and set speed to within allowed range."""
        self.speed = max(0.0, min(float(speed), PURSUER_MAX_SPEED))

    def update(self, dt: float) -> None:
        """
        Advance position using current velocity (direction and speed).
        Call after applying direction correction for this step.
        """
        self.velocity = self.direction * self.speed
        self.position = self.position + self.velocity * dt

    def get_position(self) -> Vector3D:
        """Return current position (copy)."""
        return self.position.copy()

    def get_direction(self) -> Vector3D:
        """Return current direction (copy, unit vector)."""
        return self.direction.copy()
