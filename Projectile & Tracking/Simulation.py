"""
Simulation-only main loop controller.
Fixed timestep updates and terminal rendering. No GUI.
"""

from typing import Literal

from Vector2D import Vector2D
from Missile import Missile
from Tracker import Tracker
from Target import Target
from config import (
    HIT_THRESHOLD,
    LOG_DECIMAL_PLACES,
    LOG_EVERY_N_STEPS,
    SIM_DT,
    SIM_MAX_TIME,
)

# Status: ACTIVE, HIT, or MISS (timeout / out of bounds)
SimStatus = Literal["ACTIVE", "HIT", "MISS"]


class Simulation:
    """
    Main loop: time-stepped updates, tracker-driven steering, terminal output.
    Simulation only - for educational and portfolio use.
    """

    def __init__(
        self,
        pursuer_start: Vector2D,
        target_start: Vector2D,
        target_mode: str = "linear",
    ) -> None:
        self.missile = Missile(pursuer_start, heading=0.0)
        self.target = Target(target_start, mode=target_mode)
        self.tracker = Tracker()
        self.time: float = 0.0
        self.status: SimStatus = "ACTIVE"
        self._step_count = 0

    def step(self) -> None:
        """Advance one fixed timestep. Simulation only."""
        if self.status != "ACTIVE":
            return
        # Tracker: desired heading from current positions
        desired = self.tracker.get_heading_correction_signal(
            self.missile.get_position(),
            self.missile.get_heading(),
            self.target.get_position(),
        )
        # Pursuer: gradual heading correction then move
        self.missile.apply_heading_correction(desired, SIM_DT)
        self.missile.update(SIM_DT)
        self.target.update(SIM_DT)
        self.time += SIM_DT
        self._step_count += 1
        # Check hit
        _, dist = self.tracker.compute_relative(
            self.missile.get_position(), self.target.get_position()
        )
        if dist <= HIT_THRESHOLD:
            self.status = "HIT"
        elif self.time >= SIM_MAX_TIME:
            self.status = "MISS"

    def run(self) -> SimStatus:
        """
        Run until HIT or MISS (timeout). Print terminal log each step.
        Returns final status.
        """
        self._print_header()
        while self.status == "ACTIVE":
            self._log_step()
            self.step()
        self._log_step()
        self._print_footer()
        return self.status

    def _log_step(self) -> None:
        """Print one line of structured log if step count matches LOG_EVERY_N_STEPS."""
        if self._step_count % LOG_EVERY_N_STEPS != 0 and self.status == "ACTIVE":
            return
        mp = self.missile.get_position()
        tp = self.target.get_position()
        _, dist = self.tracker.compute_relative(mp, tp)
        fmt = f".{LOG_DECIMAL_PLACES}f"
        print(
            f"t={self.time:{fmt}} | "
            f"Missile=({mp.x:{fmt}}, {mp.y:{fmt}}) | "
            f"Target=({tp.x:{fmt}}, {tp.y:{fmt}}) | "
            f"Dist={dist:{fmt}} | {self.status}"
        )

    def _print_header(self) -> None:
        """Print simulation header. Simulation only."""
        print("--- Pursuit Simulation (Simulation Only - Educational) ---")
        print(f"Timestep={SIM_DT}, Hit threshold={HIT_THRESHOLD}")
        print("-" * 60)

    def _print_footer(self) -> None:
        """Print final status."""
        print("-" * 60)
        print(f"Result: {self.status} at t={self.time:.1f}")


def main() -> None:
    """Entry point: run simulation from terminal. Simulation only."""
    pursuer_start = Vector2D(0.0, 0.0)
    target_start = Vector2D(25.0, 15.0)
    sim = Simulation(pursuer_start, target_start, target_mode="sinusoidal")
    sim.run()


if __name__ == "__main__":
    main()
