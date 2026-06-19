import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import matplotlib.patches as patches
import random
from scipy.stats import norm 

# --- 【關鍵設定】指定 FFmpeg 的路徑 ---
# 注意：最後面要加上 \ffmpeg.exe
plt.rcParams['animation.ffmpeg_path'] = r"C:\Temp\ffmpeg-2026-05-21-git-0857141823-full_build\ffmpeg-2026-05-21-git-0857141823-full_build\bin\ffmpeg.exe"

# --- 1. 影片與動畫基礎設定 ---
fig = plt.figure(figsize=(5.4, 9.6), facecolor='#101010')
ax = fig.add_axes([0.05, 0.1, 0.9, 0.8]) 
ax.set_facecolor('k')
ax.set_aspect('equal') 
ax.axis('off')

# 主標題與副標題
fig.text(0.5, 0.95, "Two Dice Rolling", ha='center', va='center', color='white', fontsize=20, fontweight='bold')
fig.text(0.5, 0.91, "Standard Deviation", ha='center', va='center', color='white', alpha=0.8, fontsize=14)
progress_text = fig.text(0.5, 0.87, '', ha='center', va='center', color='white', fontsize=12, family='monospace')

# --- 2. 參數設定 ---
num_rolls = 1000
base_duration = 9      # 掉球時間
draw_duration = 0.4    # 劃線速度
fade_duration = 2.6    # 68% 淡入與停頓
duration_seconds = base_duration + draw_duration + fade_duration
fps = 60
total_frames = int(duration_seconds * fps)
rolling_frames = int(base_duration * fps)
drawing_frames = int(draw_duration * fps)

gravity = -0.20
bin_spacing = 10
dot_radius = 0.45 
dot_diameter = 2 * dot_radius
bins_range = np.arange(2, 13)
bins_x_coords = {b: b * bin_spacing for b in bins_range}

# --- 3. 預模擬以確定高度 ---
random.seed(42)
temp_counts = {b: 0 for b in bins_range}
for _ in range(num_rolls):
    s = random.randint(1, 6) + random.randint(1, 6)
    temp_counts[s] += 1
max_h = max(temp_counts.values())
y_max = max_h * dot_diameter + 15 

ax.set_xlim(min(bins_x_coords.values()) - bin_spacing, max(bins_x_coords.values()) + bin_spacing)
ax.set_ylim(-5, y_max)

for b, x in bins_x_coords.items():
    ax.text(x, -2, str(b), ha='center', va='top', color='white', fontsize=10)

# --- 4. 數據結構與繪圖對象 ---
settled_dots = [] 
falling_dots = [] 
bin_stacks = {b: 0 for b in bins_range} 

mu, sigma = 7, np.sqrt(2 * 35/12)
x_curve = np.linspace(2, 12, 200) 
peak_prob = 6/36
y_curve = norm.pdf(x_curve, mu, sigma) * (num_rolls * peak_prob / norm.pdf(mu, mu, sigma)) * dot_diameter

curve_line, = ax.plot([], [], color='white', linewidth=2.5, zorder=6)
sd_fill = ax.fill_between(x_curve * bin_spacing, 0, y_curve, 
                         where=(x_curve >= mu-sigma) & (x_curve <= mu+sigma),
                         color='white', alpha=0, zorder=5)
sd_text_obj = ax.text(mu * bin_spacing, max(y_curve)*0.45, "68%", color='white', 
                    ha='center', fontsize=16, fontweight='bold', alpha=0, zorder=10)

random.seed(42)

# --- 5. 動畫更新函數 ---
def update(frame):
    if frame < rolling_frames:
        rolls_per_frame = int(np.ceil(num_rolls / rolling_frames))
        for _ in range(rolls_per_frame):
            if (len(settled_dots) + len(falling_dots)) < num_rolls:
                dice_sum = random.randint(1, 6) + random.randint(1, 6)
                bin_x = bins_x_coords[dice_sum]
                target_y = bin_stacks[dice_sum] * dot_diameter + dot_radius
                bin_stacks[dice_sum] += 1
                color = plt.cm.viridis((dice_sum - 2) / 10)
                circle = patches.Circle((bin_x, y_max * 0.95), dot_radius, color=color, zorder=3)
                ax.add_patch(circle)
                falling_dots.append([circle, 0.0, target_y])

    remaining_falling = []
    for dot_data in falling_dots:
        circle, vy, target_y = dot_data
        vy += gravity 
        ny = circle.center[1] + vy
        if ny <= target_y:
            circle.center = (circle.center[0], target_y)
            settled_dots.append(circle)
        else:
            circle.center = (circle.center[0], ny)
            remaining_falling.append([circle, vy, target_y])
    falling_dots[:] = remaining_falling

    if rolling_frames <= frame < (rolling_frames + drawing_frames):
        idx = int(((frame - rolling_frames) / max(1, (drawing_frames - 1))) * len(x_curve))
        curve_line.set_data(x_curve[:idx] * bin_spacing, y_curve[:idx])
    elif frame >= (rolling_frames + drawing_frames):
        curve_line.set_data(x_curve * bin_spacing, y_curve)
        fade_p = (frame - (rolling_frames + drawing_frames)) / (total_frames - (rolling_frames + drawing_frames) - 1)
        alpha_val = min(1.0, fade_p * 3)
        sd_fill.set_alpha(alpha_val * 0.25) 
        sd_text_obj.set_alpha(alpha_val)

    progress_text.set_text(f"Rolls: {min(len(settled_dots) + len(falling_dots), num_rolls)} / {num_rolls}")
    return []

# --- 6. 建立動畫 ---
my_animation = animation.FuncAnimation(
    fig, update, frames=total_frames, blit=False, repeat=False, interval=1000/fps
)

# --- 7. 【獨立儲存區塊】 ---


# 最後顯示預覽
plt.show()