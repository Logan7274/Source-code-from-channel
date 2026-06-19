import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import os

# --- 1. 設置 LaTeX 數學字體風格 (Computer Modern) ---
plt.rcParams.update({
    "mathtext.fontset": "cm", 
    "font.family": "serif",
})

# --- FFmpeg 路徑設定 ---
ffmpeg_path = r"C:\Temp\ffmpeg-2026-05-21-git-0857141823-full_build\ffmpeg-2026-05-21-git-0857141823-full_build\bin\ffmpeg.exe"
if os.path.exists(ffmpeg_path):
    plt.rcParams['animation.ffmpeg_path'] = ffmpeg_path

# --- 2. 參數設定 ---
num_points = 300
duration_seconds = 15
fps = 60
total_frames = duration_seconds * fps

# --- 3. 畫布設定 ---
plt.style.use('dark_background')
fig = plt.figure(figsize=(5.4, 9.6), facecolor='black')
ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor('black')
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.8, 1.8) 
ax.set_aspect('equal')
ax.axis('off')

# --- 4. 數學公式與標題 (修正後的語法) ---
# 主標題：使用 \mathrm 確保字體正確且不崩潰
fig.text(0.5, 0.93, r"$\mathrm{The\ Times\ Tables\ on\ a\ Circle}$", 
         ha='center', color='white', fontsize=18)

# 副標題
fig.text(0.5, 0.89, r"$\mathrm{Visualizing\ Modular\ Multiplication}$", 
         ha='center', color='#888888', fontsize=12)

# 核心公式：將 \pmod 改為 \mathrm{mod}
formula_label = fig.text(0.5, 0.84, r"$x \mapsto (x \cdot M) \mathrm{\ mod\ } N$", 
                         ha='center', color='#00FFFF', fontsize=18)

# 當前倍數標註 (使用 LaTeX 字體 $M = ...$)
multiplier_label = fig.text(0.5, 0.08, '', ha='center', color='white', 
                            fontsize=14, alpha=0.6)

# --- 5. 預計算 ---
theta = np.linspace(0, 2*np.pi, num_points, endpoint=False)
x_coords = np.cos(theta)
y_coords = np.sin(theta)

lines, = ax.plot([], [], color='#00FFFF', lw=0.5, alpha=0.4)

def ease_in_out_sine(x):
    return -(np.cos(np.pi * x) - 1) / 2

# --- 6. 動畫更新函數 ---
def update(frame):
    progress = frame / (total_frames - 1)
    eased_progress = ease_in_out_sine(progress)
    
    m = 2 + eased_progress * 98
    
    indices = np.arange(num_points)
    targets = (indices * m) % num_points
    
    all_x = []
    all_y = []
    for i in range(num_points):
        all_x.extend([x_coords[i], x_coords[int(targets[i])], None])
        all_y.extend([y_coords[i], y_coords[int(targets[i])], None])
    
    lines.set_data(all_x, all_y)
    
    # 色彩漸變
    color_val = plt.cm.plasma(eased_progress * 0.8 + 0.2)
    lines.set_color(color_val)
    formula_label.set_color(color_val)
    
    # 更新 M 的值
    multiplier_label.set_text(rf"$M = {m:.2f}$")
    
    return [lines, multiplier_label]

# 建立動畫
my_animation = animation.FuncAnimation(
    fig, update, frames=total_frames, blit=False, interval=1000/fps, repeat=False
)

# =====================================================================
# ▼▼▼ 儲存區塊 (預設註解，先跑預覽) ▼▼▼
# =====================================================================
print("正在壓製科普版『數字星雲』影片...")
output_name = "modular_science_fixed.mp4"
my_animation.save(
     output_name, fps=fps, dpi=300, 
     extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-b:v', '8000k']
 )

plt.show()