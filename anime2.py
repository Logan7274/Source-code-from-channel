import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from numpy import sin, cos

# --- 1. Simulation and Physics Parameters ---
num_pendulums = 60      # Total number of rainbow pendulums
duration_seconds = 10   # Duration of the animation loop
fps = 60                # Frames per second
total_frames = duration_seconds * fps
dt = 1.0 / fps          # Time step for numerical integration

L1, L2 = 1.0, 1.0       # Length of the first and second arms
M1, M2 = 1.0, 1.0       # Mass of the first and second bobs
G = 12.0                # Gravity constant (boosted for more dynamic motion)

# Initial conditions (in radians)
th1_init = np.pi / 1.5  # Starting angle for the first arm (~120 degrees)
th2_init = np.pi / 2    # Starting angle for the second arm (90 degrees)
epsilon = 0.02          # Tiny starting difference between pendulums (Chaos trigger)

# --- 2. Physics Engine (Runge-Kutta 4th Order) ---
def get_derivs(state):
    """Computes the derivatives of the double pendulum system state."""
    t1, w1, t2, w2 = state
    delta = t1 - t2
    den1 = (M1 + M2) * L1 - M2 * L1 * cos(delta)**2
    dw1 = (M2 * L1 * w1**2 * sin(delta) * cos(delta) +
           M2 * G * sin(t2) * cos(delta) +
           M2 * L2 * w2**2 * sin(delta) -
           (M1 + M2) * G * sin(t1)) / den1
           
    den2 = (L2 / L1) * den1
    dw2 = (-M2 * L2 * w2**2 * sin(delta) * cos(delta) +
           (M1 + M2) * G * sin(t1) * cos(delta) -
           (M1 + M2) * L1 * w1**2 * sin(delta) -
           (M1 + M2) * G * sin(t2)) / den2
           
    return np.array([w1, dw1, w2, dw2])

def rk4_step(state, dt):
    """Standard RK4 integration for stability."""
    k1 = get_derivs(state)
    k2 = get_derivs(state + 0.5 * dt * k1)
    k3 = get_derivs(state + 0.5 * dt * k2)
    k4 = get_derivs(state + dt * k3)
    return state + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

# --- 3. Pre-computing Trajectories ---
print("Calculating chaotic physics for 60 pendulums...")
all_x1 = np.zeros((num_pendulums, total_frames))
all_y1 = np.zeros((num_pendulums, total_frames))
all_x2 = np.zeros((num_pendulums, total_frames))
all_y2 = np.zeros((num_pendulums, total_frames))

for i in range(num_pendulums):
    # Every pendulum starts with a slightly different second angle
    state = np.array([th1_init, 0.0, th2_init + i * epsilon, 0.0])
    for f in range(total_frames):
        t1, w1, t2, w2 = state
        # Map polar coordinates to Cartesian
        all_x1[i, f] = L1 * sin(t1)
        all_y1[i, f] = -L1 * cos(t1)
        all_x2[i, f] = all_x1[i, f] + L2 * sin(t2)
        all_y2[i, f] = all_y1[i, f] - L2 * cos(t2)
        # Advance physics
        state = rk4_step(state, dt)

# --- 4. Animation Setup ---
plt.style.use('dark_background')
fig = plt.figure(figsize=(5.4, 9.6), facecolor='black')
# Occupy 100% of the figure space (Fullscreen)
ax = fig.add_axes([0, 0, 1, 1]) 

# --- CRITICAL FIX: Viewport calculation to avoid top-clipping ---
# In a 9:16 aspect ratio, if width is 5 units, height should be 8.88 units.
# We set x from -2.5 to 2.5 (width=5).
ax.set_xlim(-2.5, 2.5) 
# Max pendulum height is +2.0. We set Y-top to 2.8 for safe margins.
ax.set_ylim(-3.08, 2.8) 
ax.set_aspect('equal')
ax.axis('off')

# Color palette: Intense Turbo Rainbow
colors = plt.cm.turbo(np.linspace(0, 1, num_pendulums))

# Initialize plot objects
lines = [ax.plot([], [], color=colors[i], lw=1.5, alpha=0.8)[0] for i in range(num_pendulums)]
trails = [ax.plot([], [], color=colors[i], lw=1.0, alpha=0.3)[0] for i in range(num_pendulums)]
points = [ax.plot([], [], 'o', color=colors[i], markersize=5)[0] for i in range(num_pendulums)]

# --- 5. Animation Update Function ---
def update(frame):
    trail_length = 45 # Frames to keep in the trailing tail
    start = max(0, frame - trail_length)
    
    for i in range(num_pendulums):
        x1, y1 = all_x1[i, frame], all_y1[i, frame]
        x2, y2 = all_x2[i, frame], all_y2[i, frame]
        
        # Update main arms
        lines[i].set_data([0, x1, x2], [0, y1, y2])
        # Update moving bobs
        points[i].set_data([x2], [y2])
        # Update trailing light paths
        trails[i].set_data(all_x2[i, start:frame+1], all_y2[i, start:frame+1])
        
    return lines + points + trails

# Create animation object
# repeat=True allows the preview to loop indefinitely
my_animation = animation.FuncAnimation(
    fig, update, frames=total_frames, blit=True, interval=1000/fps, repeat=True
)

print("Displaying real-time preview...")
plt.show()