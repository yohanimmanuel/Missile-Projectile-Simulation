"""
Simulation-only pursuer (interceptor).
Maintains position, velocity, heading with limited turn rate and speed.
Uses simple steering logic - no real-world guidance algorithms.
"""

from Vector2D import Vector2D
from config import PURSUER_INITIAL_SPEED, PURSUER_MAX_SPEED, PURSUER_MAX_TURN_RATE


class Missile:
    """
    Pursuer entity: position, velocity, heading with max turn rate and max speed.
    Steering is gradual; no instant rotation or teleportation.
    Simulation only - fictional control logic.
    """

    def __init__(self, position: Vector2D, heading: float = 0.0) -> None:
        """
        Args:
            position: Initial position in abstract 2D space.
            heading: Initial heading in radians (0 = +X, pi/2 = +Y).
        """
        self.position = position.copy()
        self.heading = float(heading)
        self.speed = min(float(PURSUER_INITIAL_SPEED), PURSUER_MAX_SPEED)
        self.velocity = Vector2D.from_heading(self.heading, self.speed)

    def apply_heading_correction(self, desired_heading: float, dt: float) -> None:
        """
        Adjust heading toward desired_heading subject to max turn rate.
        Simulation-only steering; not a real guidance law.
        """
        # Normalize angle difference to [-pi, pi]
        diff = desired_heading - self.heading
        while diff > 3.141592653589793:
            diff -= 2 * 3.141592653589793
        while diff < -3.141592653589793:
            diff += 2 * 3.141592653589793
        max_turn = PURSUER_MAX_TURN_RATE  # per step (dt already in step)
        if diff > max_turn:
            self.heading += max_turn
        elif diff < -max_turn:
            self.heading -= max_turn
        else:
            self.heading = desired_heading

    def set_speed(self, speed: float) -> None:
        """Clamp and set speed to within allowed range."""
        self.speed = max(0.0, min(float(speed), PURSUER_MAX_SPEED))

    def update(self, dt: float) -> None:
        """
        Advance position using current velocity (heading and speed).
        Call after applying heading correction for this step.
        """
        self.velocity = Vector2D.from_heading(self.heading, self.speed)
        self.position = self.position + self.velocity * dt

    def get_position(self) -> Vector2D:
        """Return current position (copy)."""
        return self.position.copy()

    def get_heading(self) -> float:
        """Return current heading in radians."""
        return self.heading
