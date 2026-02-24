"""
Simulation-only 2D vector math.
Abstract space - no real-world units or physics constants.
"""

import math
from typing import Tuple


class Vector2D:
    """
    Represents a 2D vector for position, velocity, or acceleration
    in an abstract simulation space. Simulation only.
    """

    __slots__ = ("x", "y")

    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        self.x = float(x)
        self.y = float(y)

    def __add__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vector2D":
        return Vector2D(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> "Vector2D":
        return self * scalar

    def __repr__(self) -> str:
        return f"Vector2D({self.x}, {self.y})"

    def copy(self) -> "Vector2D":
        """Return a new vector with the same components."""
        return Vector2D(self.x, self.y)

    def magnitude(self) -> float:
        """Return the length of the vector (abstract units)."""
        return math.sqrt(self.x * self.x + self.y * self.y)

    def normalized(self) -> "Vector2D":
        """Return a unit vector in the same direction, or zero vector if length is 0."""
        mag = self.magnitude()
        if mag < 1e-10:
            return Vector2D(0.0, 0.0)
        return Vector2D(self.x / mag, self.y / mag)

    def dot(self, other: "Vector2D") -> float:
        """Dot product."""
        return self.x * other.x + self.y * other.y

    def as_tuple(self) -> Tuple[float, float]:
        """Return (x, y) tuple."""
        return (self.x, self.y)

    @staticmethod
    def from_heading(heading_rad: float, length: float = 1.0) -> "Vector2D":
        """
        Create a vector from an angle (radians, 0 = +X, pi/2 = +Y)
        and optional length. Simulation-only convention.
        """
        return Vector2D(length * math.cos(heading_rad), length * math.sin(heading_rad))

    def to_heading(self) -> float:
        """
        Return angle in radians for this vector (0 = +X, pi/2 = +Y).
        Returns 0 if vector has zero length.
        """
        if abs(self.x) < 1e-10 and abs(self.y) < 1e-10:
            return 0.0
        return math.atan2(self.y, self.x)

    def clamp_magnitude(self, max_mag: float) -> "Vector2D":
        """Return a vector with magnitude capped at max_mag."""
        mag = self.magnitude()
        if mag <= max_mag or mag < 1e-10:
            return self.copy()
        return self.normalized() * max_mag
