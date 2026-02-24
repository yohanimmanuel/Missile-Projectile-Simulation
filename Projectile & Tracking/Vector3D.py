"""
Simulation-only 3D vector math.
Abstract space - no real-world units or physics constants.
"""

import math
from typing import Tuple

PI = 3.141592653589793
EPS = 1e-10


class Vector3D:
    """
    Represents a 3D vector for position, velocity, or direction
    in an abstract simulation space. Simulation only.
    """

    __slots__ = ("x", "y", "z")

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __add__(self, other: "Vector3D") -> "Vector3D":
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vector3D") -> "Vector3D":
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> "Vector3D":
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)

    def __rmul__(self, scalar: float) -> "Vector3D":
        return self * scalar

    def __repr__(self) -> str:
        return f"Vector3D({self.x}, {self.y}, {self.z})"

    def copy(self) -> "Vector3D":
        """Return a new vector with the same components."""
        return Vector3D(self.x, self.y, self.z)

    def magnitude(self) -> float:
        """Return the length of the vector (abstract units)."""
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalized(self) -> "Vector3D":
        """Return a unit vector in the same direction, or zero vector if length is 0."""
        mag = self.magnitude()
        if mag < EPS:
            return Vector3D(1.0, 0.0, 0.0)
        return Vector3D(self.x / mag, self.y / mag, self.z / mag)

    def dot(self, other: "Vector3D") -> float:
        """Dot product."""
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: "Vector3D") -> "Vector3D":
        """Cross product."""
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def as_tuple(self) -> Tuple[float, float, float]:
        """Return (x, y, z) tuple."""
        return (self.x, self.y, self.z)

    def clamp_magnitude(self, max_mag: float) -> "Vector3D":
        """Return a vector with magnitude capped at max_mag."""
        mag = self.magnitude()
        if mag <= max_mag or mag < EPS:
            return self.copy()
        return self.normalized() * max_mag

    def rotate_toward(self, desired: "Vector3D", max_angle_rad: float) -> "Vector3D":
        """
        Return a unit vector that is current direction rotated toward desired
        by at most max_angle_rad. Simulation-only steering helper.
        If current or desired is zero-length, returns desired.normalized() or current.
        """
        d = desired.normalized()
        c = self.normalized()
        if c.magnitude() < EPS:
            return d
        if d.magnitude() < EPS:
            return c
        dot_val = max(-1.0, min(1.0, c.dot(d)))
        angle = math.acos(dot_val)
        if angle <= max_angle_rad or angle < EPS:
            return d
        # Slerp: c * sin(angle - max_angle) + d * sin(max_angle) over sin(angle)
        sin_angle = math.sin(angle)
        if sin_angle < EPS:
            return d
        t = max_angle_rad / angle
        s0 = math.sin((1.0 - t) * angle)
        s1 = math.sin(t * angle)
        return (c * s0 + d * s1).normalized()