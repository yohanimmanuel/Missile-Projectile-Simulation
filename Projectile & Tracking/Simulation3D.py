"""
Simulation-only 3D main loop controller.
Fixed timestep updates and terminal rendering. No GUI.
"""

from typing import Literal

from Vector3D import Vector3D
from Missile3D import Missile3D
from Tracker3D import Tracker3D
from Target3D import Target3D
from config import (
    HIT_THRESHOLD,
    LOG_DECIMAL_PLACES,
    LOG_EVERY_N_STEPS,
    SIM_DT,
    SIM_MAX_TIME,
)

SimStatus = Literal["ACTIVE", "HIT", "MISS"]


class Simulation3D:
    """
    Main loop for 3D: time-stepped updates, tracker-driven steering, terminal output.
    Simulation only - for educational and portfolio use.
    """

    def __init__(
        self,
        pursuer_start: Vector3D,
        target_start: Vector3D,
        target_mode: str = "linear",
    ) -> None:
        self.missile = Missile3D(pursuer_start, direction=Vector3D(1.0, 0.0, 0.0))
        self.target = Target3D(target_start, mode=target_mode)
        self.tracker = Tracker3D()
        self.time: float = 0.0
        self.status: SimStatus = "ACTIVE"
        self._step_count = 0

    def step(self) -> None:
        """Advance one fixed timestep. Simulation only."""
        if self.status != "ACTIVE":
            return
        desired = self.tracker.get_direction_correction_signal(
            self.missile.get_position(),
            self.missile.get_direction(),
            self.target.get_position(),
        )
        self.missile.apply_direction_correction(desired, SIM_DT)
        self.missile.update(SIM_DT)
        self.target.update(SIM_DT)
        self.time += SIM_DT
        self._step_count += 1
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
            f"Missile=({mp.x:{fmt}}, {mp.y:{fmt}}, {mp.z:{fmt}}) | "
            f"Target=({tp.x:{fmt}}, {tp.y:{fmt}}, {tp.z:{fmt}}) | "
            f"Dist={dist:{fmt}} | {self.status}"
        )

    def _print_header(self) -> None:
        """Print simulation header. Simulation only."""
        print("--- 3D Pursuit Simulation (Simulation Only - Educational) ---")
        print(f"Timestep={SIM_DT}, Hit threshold={HIT_THRESHOLD}")
        print("-" * 72)

    def _print_footer(self) -> None:
        """Print final status."""
        print("-" * 72)
        print(f"Result: {self.status} at t={self.time:.1f}")


def main() -> None:
    """Entry point: run 3D simulation from terminal. Simulation only."""
    pursuer_start = Vector3D(0.0, 0.0, 0.0)
    target_start = Vector3D(25.0, 15.0, 10.0)
    sim = Simulation3D(pursuer_start, target_start, target_mode="sinusoidal")
    sim.run()


if __name__ == "__main__":
    main()
