"""
Simulation-only tracker.
Observes target position and produces a desired heading correction signal.
Does not use real-world guidance laws - abstract pursuit logic only.
"""

from Vector2D import Vector2D


class Tracker:
    """
    Observes target position and computes relative vector (distance and direction).
    Produces desired heading correction for the pursuer. Simulation only.
    """

    def __init__(self) -> None:
        self._last_target_position: Vector2D | None = None

    def compute_relative(self, pursuer_pos: Vector2D, target_pos: Vector2D) -> tuple[Vector2D, float]:
        """
        Compute vector from pursuer to target and its length.
        Simulation only - no real targeting logic.

        Returns:
            (direction_to_target as unit vector, distance)
        """
        delta = target_pos - pursuer_pos
        distance = delta.magnitude()
        if distance < 1e-10:
            return Vector2D(1.0, 0.0), 0.0
        direction = delta.normalized()
        return direction, distance

    def desired_heading(self, pursuer_pos: Vector2D, target_pos: Vector2D) -> float:
        """
        Compute desired heading (radians) for pursuer to point toward target.
        Used as setpoint for steering only - not a real guidance law.
        """
        direction, _ = self.compute_relative(pursuer_pos, target_pos)
        return direction.to_heading()

    def get_heading_correction_signal(
        self, pursuer_pos: Vector2D, pursuer_heading: float, target_pos: Vector2D
    ) -> float:
        """
        Produce desired heading (radians) for the pursuer based on target position.
        The pursuer uses this with its max turn rate for gradual steering.
        Simulation only.
        """
        return self.desired_heading(pursuer_pos, target_pos)
