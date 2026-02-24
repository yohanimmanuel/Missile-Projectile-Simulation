# Pursuit Projectile Simulation

**This is a simulation for educational and portfolio purposes only.** It is not a real weapon system. No real missile guidance algorithms, military parameters, or targeting systems are used. All values and behaviors are abstract and fictional.

## What This Demonstrates

- **Software architecture**: Clear separation between pursuer (Missile), target (Target), tracker (Tracker), and simulation loop (Simulation).
- **Control logic**: Simple steering with a desired heading and limited turn rate (no instant rotation).
- **Math abstraction**: 2D/3D vectors for position, velocity, and heading/direction in an abstract space (3D uses direction vectors and spherical-style turn limits).
- **Simulation design**: Fixed timestep updates, configurable constants, terminal-only output.

## How to Run (Terminal)

From the project directory:

**2D simulation:**
```bash
python Simulation.py
```

**3D simulation (terminal log):**
```bash
python Simulation3D.py
```

**3D simulation with pop-up view (engagement geometry style):**  
Shows a 3D window with launch point, interceptor trajectory (orange), maneuvering target trajectory (red), and hit marker (yellow). Requires `matplotlib`.
```bash
pip install -r requirements.txt
python Simulation3D_Visual.py
```

### 2D example output

```
--- Pursuit Simulation (Simulation Only - Educational) ---
Timestep=0.1, Hit threshold=1.0
------------------------------------------------------------
t=0.0 | Missile=(0.0, 0.0) | Target=(25.0, 15.0) | Dist=29.2 | ACTIVE
t=0.1 | Missile=(0.3, 0.0) | Target=(25.1, 15.1) | Dist=29.0 | ACTIVE
...
t=12.4 | Missile=(23.1, 9.8) | Target=(30.2, 14.6) | Dist=8.3 | ACTIVE
...
------------------------------------------------------------
Result: HIT at t=...
```

### 3D example output

```
--- 3D Pursuit Simulation (Simulation Only - Educational) ---
Timestep=0.1, Hit threshold=1.0
------------------------------------------------------------------------
t=0.0 | Missile=(0.0, 0.0, 0.0) | Target=(25.0, 15.0, 10.0) | Dist=30.8 | ACTIVE
...
t=14.2 | Missile=(22.1, 11.3, 8.1) | Target=(28.4, 14.2, 11.0) | Dist=7.2 | ACTIVE
...
------------------------------------------------------------------------
Result: HIT at t=...
```

## Project Layout

| File            | Purpose |
|-----------------|--------|
| `config.py`     | Tunable constants (all fictional; shared by 2D and 3D). |
| **2D**          | |
| `Vector2D.py`   | 2D position, velocity, heading math. |
| `Target.py`     | Moving object: linear, sinusoidal, random. |
| `Missile.py`    | Pursuer: heading, max turn rate, max speed, gradual steering. |
| `Tracker.py`    | Relative vector and desired heading. |
| `Simulation.py` | 2D main loop and terminal output. |
| **3D**          | |
| `Vector3D.py`   | 3D position, velocity, direction; `rotate_toward` for steering. |
| `Target3D.py`   | 3D moving object: linear, sinusoidal, random. |
| `Missile3D.py`  | Pursuer: direction vector, max turn rate, max speed. |
| `Tracker3D.py`  | Relative vector and desired direction (unit vector). |
| `Simulation3D.py` | 3D main loop and terminal output. |
| `Simulation3D_Visual.py` | 3D pop-up: engagement view with trajectories and hit marker (needs matplotlib). |

## Configuration

Edit `config.py` to change:

- `SIM_DT`, `SIM_MAX_TIME`, `HIT_THRESHOLD`
- Pursuer: `PURSUER_MAX_SPEED`, `PURSUER_MAX_TURN_RATE`, `PURSUER_INITIAL_SPEED`
- Target: speeds, sinusoidal amplitude/frequency, random step scale
- Logging: `LOG_DECIMAL_PLACES`, `LOG_EVERY_N_STEPS`

## Target Modes

In both `Simulation.py` (2D) and `Simulation3D.py` (3D) you can pass `target_mode="linear"`, `"sinusoidal"`, or `"random"` when creating the simulation to change how the target moves.

## Requirements

- Python 3.9+
- **Terminal runs:** no extra dependencies.
- **3D pop-up view:** `matplotlib` (see `requirements.txt`).

## Disclaimer

This project is for learning and portfolio use only. It does not implement real-world guidance, physics, or military systems. All logic and constants are abstract and documented as simulation-only.
