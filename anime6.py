import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import os

# --- 1. Environment Configuration ---
# Define the path to your FFmpeg executable for high-quality video rendering
ffmpeg_path = r"C:\Temp\ffmpeg-2026-05-21-git-0857141823-full_build\ffmpeg-2026-05-21-git-0857141823-full_build\bin\ffmpeg.exe"
if os.path.exists(ffmpeg_path):
    plt.rcParams['animation.ffmpeg_path'] = ffmpeg_path

# --- 2. Animation Parameters ---
duration_seconds = 10      # Duration of the video clip
fps = 60                   # Frames per second for smooth motion
total_frames = duration_seconds * fps
num_particles = 60000      # Number of points to calculate (higher = more detailed/silk-like)

# --- 3. Canvas Setup (Portrait 9:16) ---
# Set the background to dark for a high-contrast cinematic look
plt.style.use('dark_background')
# Define a 5.4 x 9.6 inch figure (results in 1080x1920 pixels at 200 DPI)
fig = plt.figure(figsize=(5.4, 9.6), facecolor='black')
# Add an axes that occupies 100% of the figure space (Fullscreen)
ax = fig.add_axes([0, 0, 1, 1]) 
ax.set_facecolor('black')
ax.set_aspect('equal')     # Ensure the attractor isn't distorted
ax.axis('off')             # Hide axes and labels for a pure visual experience

# --- 4. Initialize Plotting Object ---
# Use a scatter plot for particles. 's' is the size, 'alpha' is transparency for overlapping glow
scat = ax.scatter([], [], s=0.03, color='#00FFFF', alpha=0.5, edgecolors='none')
scat.set_clip_on(False)    # Prevent particles from being cut off at the coordinate boundaries

# --- 5. Core Mathematical Function ---
def get_attractor_points(a, b, c, d, n):
    """
    Computes the iterative map for the Clifford Attractor.
    Equations:
    x_n+1 = sin(a*y_n) + c*cos(a*x_n)
    y_n+1 = sin(b*x_n) + d*cos(b*y_n)
    """
    x, y = np.zeros(n), np.zeros(n)
    curr_x, curr_y = 0.1, 0.1  # Starting seed point
    for i in range(n):
        next_x = np.sin(a * curr_y) + c * np.cos(a * curr_x)
        next_y = np.sin(b * curr_x) + d * np.cos(b * curr_y)
        x[i], y[i] = next_x, next_y
        curr_x, curr_y = next_x, next_y
    return x, y

# --- 6. Animation Update Loop ---
def update(frame):
    # progress goes from 0.0 to 1.0
    progress = frame / total_frames
    # angle goes from 0 to 2*pi to ensure a perfect seamless loop
    angle = progress * 2 * np.pi
    
    # Parametric oscillation: Change a, b, c, d over time using Sine/Cosine
    # These coefficients determine the "dance" or morphing of the shape
    a = 1.6 + np.sin(angle) * 0.9
    b = 1.5 + np.cos(angle) * 1.0
    c = 1.4 + np.sin(angle * 1.5) * 0.7
    d = 1.6 + np.cos(angle) * 0.8
    
    # Calculate new particle coordinates for this frame
    x, y = get_attractor_points(a, b, c, d, num_particles)
    scat.set_offsets(np.c_[x, y])
    
    # Dynamic Color Shift: Morph colors using the 'magma' colormap
    color_val = plt.cm.magma(0.3 + 0.6 * progress)
    scat.set_color(color_val)
    
    # Dynamic Auto-Zoom: Adjust the view limits based on the current size of the attractor
    # This keeps the visual "full" even when the shape expands or shrinks
    limit_x = (1 + abs(c)) * 1.1
    limit_y = (1 + abs(d)) * 1.1
    ax.set_xlim(-limit_x, limit_x)
    ax.set_ylim(-limit_y, limit_y) 
    
    return [scat]

# --- 7. Create Animation Object ---
# repeat=True allows the preview window to loop infinitely
my_animation = animation.FuncAnimation(
    fig, update, frames=total_frames, blit=False, interval=1000/fps, repeat=True
)


plt.show()