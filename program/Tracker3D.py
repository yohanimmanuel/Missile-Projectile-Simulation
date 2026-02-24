"""
Simulation-only tracker in 3D.
Observes target position and produces a desired direction correction signal.
Does not use real-world guidance laws - abstract pursuit logic only.
"""

from Vector3D import Vector3D


class Tracker3D:
    """
    Observes target position and computes relative vector (distance and direction).
    Produces desired direction for the pursuer. Simulation only.
    """

    def compute_relative(
        self, pursuer_pos: Vector3D, target_pos: Vector3D
    ) -> tuple[Vector3D, float]:
        """
        Compute vector from pursuer to target and its length.
        Simulation only - no real targeting logic.

        Returns:
            (direction_to_target as unit vector, distance)
        """
        delta = target_pos - pursuer_pos
        distance = delta.magnitude()
        if distance < 1e-10:
            return Vector3D(1.0, 0.0, 0.0), 0.0
        direction = delta.normalized()
        return direction, distance

    def desired_direction(
        self, pursuer_pos: Vector3D, target_pos: Vector3D
    ) -> Vector3D:
        """
        Compute desired direction (unit vector) for pursuer to point toward target.
        Used as setpoint for steering only - not a real guidance law.
        """
        direction, _ = self.compute_relative(pursuer_pos, target_pos)
        return direction

    def get_direction_correction_signal(
        self,
        pursuer_pos: Vector3D,
        pursuer_direction: Vector3D,
        target_pos: Vector3D,
    ) -> Vector3D:
        """
        Produce desired direction (unit vector) for the pursuer based on target position.
        The pursuer uses this with its max turn rate for gradual steering.
        Simulation only.
        """
        return self.desired_direction(pursuer_pos, target_pos)
