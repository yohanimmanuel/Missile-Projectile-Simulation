"""
Simulation-only 3D visual pop-up.
Runs the same pursuit simulation and displays an engagement-geometry style
3D view: launch point, interceptor and target trajectories, hit marker.
Simulation only - for educational and portfolio use.
"""

import random

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import numpy as np

from Vector3D import Vector3D
from Missile3D import Missile3D
from Tracker3D import Tracker3D
from Target3D import Target3D
from config import (
    ARENA_X_MAX,
    ARENA_X_MIN,
    ARENA_Y_MAX,
    ARENA_Y_MIN,
    ARENA_Z_MAX,
    ARENA_Z_MIN,
    HIT_THRESHOLD,
    SIM_DT,
    SIM_MAX_TIME,
)


def _random_arena_position() -> Vector3D:
    """Return a random position in the full arena so the simulation uses the whole 3D view."""
    return Vector3D(
        random.uniform(ARENA_X_MIN, ARENA_X_MAX),
        random.uniform(ARENA_Y_MIN, ARENA_Y_MAX),
        random.uniform(ARENA_Z_MIN, ARENA_Z_MAX),
    )


def run_simulation_and_record(
    pursuer_start: Vector3D,
    target_start: Vector3D,
    target_mode: str = "linear",
    random_mode_switch: bool = True,
):
    """
    Run 3D pursuit with multiple hit opportunities: on each hit, record position,
    target escapes to new arena position, missile resets to launch, then continue until time limit.
    Returns (missile_xyz, target_xyz, hit_positions, hit_frames, status).
    Simulation only.
    """
    missile = Missile3D(pursuer_start, direction=Vector3D(1.0, 0.0, 0.0))
    target = Target3D(target_start, mode=target_mode, mode_schedule="fixed")
    tracker = Tracker3D()

    missile_hist = [[pursuer_start.x, pursuer_start.y, pursuer_start.z]]
    target_hist = [[target_start.x, target_start.y, target_start.z]]
    hit_positions: list[list[float]] = []
    hit_frames: list[int] = []
    time_val = 0.0
    status = "ACTIVE"
    step_count = 0
    target.set_direction_toward(_random_arena_position())
    next_switch_at = random.randint(50, 150)

    while status == "ACTIVE":
        if random_mode_switch and step_count >= next_switch_at:
            waypoint = _random_arena_position()
            target.set_direction_toward(waypoint)
            next_switch_at = step_count + random.randint(80, 200)
        step_count += 1

        desired = tracker.get_direction_correction_signal(
            missile.get_position(),
            missile.get_direction(),
            target.get_position(),
        )
        missile.apply_direction_correction(desired, SIM_DT)
        missile.update(SIM_DT)
        target.update(SIM_DT)
        time_val += SIM_DT

        mp = missile.get_position()
        tp = target.get_position()
        if tp.x < ARENA_X_MIN or tp.x > ARENA_X_MAX or tp.y < ARENA_Y_MIN or tp.y > ARENA_Y_MAX or tp.z < ARENA_Z_MIN or tp.z > ARENA_Z_MAX:
            target.set_direction_toward(_random_arena_position())
        missile_hist.append([mp.x, mp.y, mp.z])
        target_hist.append([tp.x, tp.y, tp.z])

        _, dist = tracker.compute_relative(mp, tp)
        if dist <= HIT_THRESHOLD:
            hit_frames.append(len(missile_hist) - 1)
            hit_positions.append([
                (mp.x + tp.x) / 2,
                (mp.y + tp.y) / 2,
                (mp.z + tp.z) / 2,
            ])
            target.position = _random_arena_position()
            target.set_direction_toward(_random_arena_position())
            missile.position = pursuer_start.copy()
            missile.direction = Vector3D(1.0, 0.0, 0.0)
        if time_val >= SIM_MAX_TIME:
            status = "MISS"
            break
    if hit_positions:
        status = "HIT"
    return np.array(missile_hist), np.array(target_hist), hit_positions, hit_frames, status


def _draw_axes(ax: Axes3D, scale: float) -> None:
    """Draw simple X,Y,Z axes from origin. Simulation only."""
    ax.plot([0, scale], [0, 0], [0, 0], "k-", linewidth=1, alpha=0.6)
    ax.plot([0, 0], [0, scale], [0, 0], "k-", linewidth=1, alpha=0.6)
    ax.plot([0, 0], [0, 0], [0, scale], "k-", linewidth=1, alpha=0.6)


def show_engagement_3d(
    missile_xyz: np.ndarray,
    target_xyz: np.ndarray,
    hit_positions: list[list[float]],
    hit_frames: list[int],
    status: str,
    animate: bool = True,
) -> None:
    """
    Open a 3D pop-up: multiple hit opportunities (yellow star at each hit).
    Simulation only.
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")

    n = len(missile_xyz)
    max_extent = max(
        np.ptp(missile_xyz) + np.ptp(target_xyz),
        1.0,
    )
    axis_scale = max_extent * 0.15

    # Launch position (first point)
    ax.scatter(
        [missile_xyz[0, 0]],
        [missile_xyz[0, 1]],
        [missile_xyz[0, 2]],
        color="gray",
        s=80,
        marker="o",
        label="Launch",
        edgecolors="black",
        linewidths=0.5,
    )

    # Trajectory lines (updated each frame)
    line_missile, = ax.plot(
        missile_xyz[0:1, 0],
        missile_xyz[0:1, 1],
        missile_xyz[0:1, 2],
        color="#e67e22",
        linewidth=2,
        label="Interceptor",
    )
    line_target, = ax.plot(
        target_xyz[0:1, 0],
        target_xyz[0:1, 1],
        target_xyz[0:1, 2],
        color="#c0392b",
        linewidth=2,
        label="Maneuvering target",
    )
    pt_missile, = ax.plot(
        [missile_xyz[0, 0]],
        [missile_xyz[0, 1]],
        [missile_xyz[0, 2]],
        color="#e67e22",
        marker="^",
        markersize=10,
        linestyle="",
        markeredgecolor="black",
        markeredgewidth=0.5,
    )
    pt_target, = ax.plot(
        [target_xyz[0, 0]],
        [target_xyz[0, 1]],
        [target_xyz[0, 2]],
        color="#2980b9",
        marker="s",
        markersize=10,
        linestyle="",
        markeredgecolor="black",
        markeredgewidth=0.5,
    )
    hit_marker, = ax.plot(
        [], [], [],
        color="gold",
        marker="*",
        markersize=25,
        linestyle="",
        markeredgecolor="orange",
        markeredgewidth=1,
        label="Hit" if not hit_positions else f"Hit ({len(hit_positions)} opportunities)",
        zorder=10,
    )

    _draw_axes(ax, axis_scale)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("Missile Projectile Simulation - nothing personal just a kind of real-world application", fontsize=11)
    ax.legend(loc="upper left", fontsize=8)

    # Full arena so the whole graphics is used
    margin = 1.0
    ax.set_xlim(0 - margin, ARENA_X_MAX + margin)
    ax.set_ylim(0 - margin, ARENA_Y_MAX + margin)
    ax.set_zlim(0 - margin, ARENA_Z_MAX + margin)
    ax.set_box_aspect([ARENA_X_MAX, ARENA_Y_MAX, ARENA_Z_MAX])

    # Engagement-geometry style view (isometric-like)
    ax.view_init(elev=20, azim=45)

    def update(frame: int) -> tuple:
        up = frame + 1
        line_missile.set_data(missile_xyz[:up, 0], missile_xyz[:up, 1])
        line_missile.set_3d_properties(missile_xyz[:up, 2])
        line_target.set_data(target_xyz[:up, 0], target_xyz[:up, 1])
        line_target.set_3d_properties(target_xyz[:up, 2])
        pt_missile.set_data([missile_xyz[frame, 0]], [missile_xyz[frame, 1]])
        pt_missile.set_3d_properties([missile_xyz[frame, 2]])
        pt_target.set_data([target_xyz[frame, 0]], [target_xyz[frame, 1]])
        pt_target.set_3d_properties([target_xyz[frame, 2]])
        by_now = [i for i in range(len(hit_frames)) if hit_frames[i] <= frame]
        if by_now:
            xs = [hit_positions[i][0] for i in by_now]
            ys = [hit_positions[i][1] for i in by_now]
            zs = [hit_positions[i][2] for i in by_now]
            hit_marker.set_data(xs, ys)
            hit_marker.set_3d_properties(zs)
        else:
            hit_marker.set_data([], [])
            hit_marker.set_3d_properties([])
        return (line_missile, line_target, pt_missile, pt_target, hit_marker)

    if animate and n > 1:
        ani = animation.FuncAnimation(
            fig,
            update,
            frames=n,
            interval=40,
            blit=False,
            repeat=True,
        )
    else:
        update(n - 1)

    plt.tight_layout()
    plt.show()


def main() -> None:
    """Run simulation and show 3D engagement view in a pop-up. Simulation only."""
    pursuer_start = Vector3D(0.0, 0.0, 0.0)
    target_start = _random_arena_position()
    missile_xyz, target_xyz, hit_positions, hit_frames, status = run_simulation_and_record(
        pursuer_start,
        target_start,
        target_mode="linear",
        random_mode_switch=True,
    )
    n_hits = len(hit_positions)
    print(f"Simulation finished: {status}" + (f" — {n_hits} hit opportunity/opportunities" if n_hits else ""))
    show_engagement_3d(missile_xyz, target_xyz, hit_positions, hit_frames, status, animate=True)


if __name__ == "__main__":
    main()
