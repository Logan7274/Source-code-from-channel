import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import matplotlib.patches as patches
import random
from scipy.stats import norm 

# --- 1. Environment Configuration ---
# Path to the FFmpeg executable for video rendering (kept for reference)
plt.rcParams['animation.ffmpeg_path'] = r"C:\Temp\ffmpeg-2026-05-21-git-0857141823-full_build\ffmpeg-2026-05-21-git-0857141823-full_build\bin\ffmpeg.exe"

# --- 2. Figure and Axes Setup (Shorts 9:16 Aspect Ratio) ---
fig = plt.figure(figsize=(5.4, 9.6), facecolor='#101010')
# Main drawing area: [left, bottom, width, height]
ax = fig.add_axes([0.05, 0.1, 0.9, 0.8]) 
ax.set_facecolor('k')
ax.set_aspect('equal') 
ax.axis('off')

# Titles and Information Labels
fig.text(0.5, 0.95, "Two Dice Rolling", ha='center', va='center', color='white', fontsize=20, fontweight='bold')
fig.text(0.5, 0.91, "Standard Deviation", ha='center', va='center', color='white', alpha=0.8, fontsize=14)
progress_text = fig.text(0.5, 0.87, '', ha='center', va='center', color='white', fontsize=12, family='monospace')

# --- 3. Simulation and Physics Parameters ---
num_rolls = 1000
base_duration = 9      # Duration for the balls to fall
draw_duration = 0.4    # Speed of the bell curve line drawing
fade_duration = 2.6    # Duration for the 68% SD region to fade in
duration_seconds = base_duration + draw_duration + fade_duration
fps = 60
total_frames = int(duration_seconds * fps)
rolling_frames = int(base_duration * fps)
drawing_frames = int(draw_duration * fps)

gravity = -0.20        # Gravity acceleration
bin_spacing = 10       # Horizontal gap between columns (bins 2-12)
dot_radius = 0.45      # Size of the balls
dot_diameter = 2 * dot_radius
bins_range = np.arange(2, 13)
bins_x_coords = {b: b * bin_spacing for b in bins_range}

# --- 4. Pre-simulation for Auto-Scaling ---
# We simulate the rolls beforehand to find the maximum stack height
random.seed(42)
temp_counts = {b: 0 for b in bins_range}
for _ in range(num_rolls):
    s = random.randint(1, 6) + random.randint(1, 6)
    temp_counts[s] += 1
max_h = max(temp_counts.values())
# Set Y-limit dynamically based on the maximum stack + top margin
y_max = max_h * dot_diameter + 15 

ax.set_xlim(min(bins_x_coords.values()) - bin_spacing, max(bins_x_coords.values()) + bin_spacing)
ax.set_ylim(-5, y_max)

# Draw bin labels (2 to 12) at the bottom
for b, x in bins_x_coords.items():
    ax.text(x, -2, str(b), ha='center', va='top', color='white', fontsize=10)

# --- 5. Initialization of Plot Objects ---
settled_dots = []        # Particles that have landed
falling_dots = []        # Particles currently in motion
bin_stacks = {b: 0 for b in bins_range} # Current count per bin

# Mathematical preparation for the Bell Curve
mu, sigma = 7, np.sqrt(2 * 35/12)
x_curve = np.linspace(2, 12, 200) 
peak_prob = 6/36 # Probability of rolling a 7
# Scale the theoretical curve to match the visual dot stacks
y_curve = norm.pdf(x_curve, mu, sigma) * (num_rolls * peak_prob / norm.pdf(mu, mu, sigma)) * dot_diameter

# Theoretical normal distribution line
curve_line, = ax.plot([], [], color='white', linewidth=2.5, zorder=6)

# Shaded area for +/- 1 Standard Deviation (68%)
sd_fill = ax.fill_between(x_curve * bin_spacing, 0, y_curve, 
                         where=(x_curve >= mu-sigma) & (x_curve <= mu+sigma),
                         color='white', alpha=0, zorder=5)

# Label for the 68% region (Set to zorder 10 to stay on top)
sd_text_obj = ax.text(mu * bin_spacing, max(y_curve)*0.45, "68%", color='white', 
                    ha='center', fontsize=16, fontweight='bold', alpha=0, zorder=10)

random.seed(42) # Reset seed for consistent animation

# --- 6. Animation Update Function ---
def update(frame):
    # Phase 1: Ball Generation (0 - 9 seconds)
    if frame < rolling_frames:
        rolls_per_frame = int(np.ceil(num_rolls / rolling_frames))
        for _ in range(rolls_per_frame):
            if (len(settled_dots) + len(falling_dots)) < num_rolls:
                dice_sum = random.randint(1, 6) + random.randint(1, 6)
                bin_x = bins_x_coords[dice_sum]
                # Calculate precise landing y-coordinate
                target_y = bin_stacks[dice_sum] * dot_diameter + dot_radius
                bin_stacks[dice_sum] += 1
                
                # Apply Viridis color mapping based on sum (2-12)
                color = plt.cm.viridis((dice_sum - 2) / 10)
                circle = patches.Circle((bin_x, y_max * 0.95), dot_radius, color=color, zorder=3)
                ax.add_patch(circle)
                falling_dots.append([circle, 0.0, target_y])

    # Phase 2: Physics Update (Gravity and Collision)
    remaining_falling = []
    for dot_data in falling_dots:
        circle, vy, target_y = dot_data
        vy += gravity 
        new_y = circle.center[1] + vy
        if new_y <= target_y:
            circle.center = (circle.center[0], target_y)
            settled_dots.append(circle)
        else:
            circle.center = (circle.center[0], new_y)
            remaining_falling.append([circle, vy, target_y])
    falling_dots[:] = remaining_falling

    # Phase 3: Post-Simulation Effects (Bell Curve and SD Fade)
    # A. Draw line from left to right (9s - 9.4s)
    if rolling_frames <= frame < (rolling_frames + drawing_frames):
        draw_progress = (frame - rolling_frames) / max(1, (drawing_frames - 1))
        idx = int(draw_progress * len(x_curve))
        curve_line.set_data(x_curve[:idx] * bin_spacing, y_curve[:idx])
    
    # B. Fade in the 68% SD region (9.4s - 12s)
    elif frame >= (rolling_frames + drawing_frames):
        curve_line.set_data(x_curve * bin_spacing, y_curve)
        fade_progress = (frame - (rolling_frames + drawing_frames)) / (total_frames - (rolling_frames + drawing_frames) - 1)
        # Accelerate the fade effect
        alpha_val = min(1.0, fade_progress * 3)
        sd_fill.set_alpha(alpha_val * 0.25) 
        sd_text_obj.set_alpha(alpha_val)

    # Update UI counter
    total_dots = len(settled_dots) + len(falling_dots)
    progress_text.set_text(f"Rolls: {min(total_dots, num_rolls)} / {num_rolls}")
    
    return []

# --- 7. Create Animation ---
# repeat=False ensures the animation stops at the perfect bell curve result
my_animation = animation.FuncAnimation(
    fig, update, frames=total_frames, blit=False, repeat=False, interval=1000/fps
)

# Start real-time preview
print("Displaying real-time physics model...")
plt.show()