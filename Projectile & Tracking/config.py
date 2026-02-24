"""
Simulation-only configuration.
All values are fictional and for educational/portfolio use only.
No real-world missile or targeting parameters.
"""

# -----------------------------------------------------------------------------
# SIMULATION ONLY - FICTIONAL CONSTANTS - NOT FOR REAL-WORLD USE
# -----------------------------------------------------------------------------

# Time stepping
SIM_DT = 0.1  # Fixed timestep (abstract time units)
SIM_MAX_TIME = 100.0  # Maximum simulation duration
HIT_THRESHOLD = 1.0  # Distance below which intercept is considered successful

# Pursuer (Interceptor) limits - abstract units
PURSUER_MAX_SPEED = 6.5
PURSUER_MAX_TURN_RATE = 0.15  # Radians per time step (abstract)
PURSUER_INITIAL_SPEED = 4.5

# Target movement - abstract units (fighter-jet style: curves and weaves, not straight lines)
TARGET_LINEAR_SPEED = 3.5
TARGET_RANDOM_SEED = None  # None = use system time for variety
# Wobble/jitter so target flies in random curved ways, not straight (simulation only)
TARGET_WOBBLE_AMPLITUDE = 1.2
TARGET_WOBBLE_FREQUENCY = 0.35
TARGET_JITTER = 0.06  # Small random heading nudge per step (radians) for irregular paths

# Terminal display
LOG_DECIMAL_PLACES = 1
LOG_EVERY_N_STEPS = 1  # Log every N steps (1 = every step)

# 3D visual: arena bounds so the simulation uses the whole graphics (abstract units)
ARENA_X_MIN = 5
ARENA_X_MAX = 40
ARENA_Y_MIN = 5
ARENA_Y_MAX = 40
ARENA_Z_MIN = 5
ARENA_Z_MAX = 30
