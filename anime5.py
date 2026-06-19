import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import os

# --- 1. 設置 LaTeX 字體風格 ---
plt.rcParams.update({
    "mathtext.fontset": "cm",
    "font.family": "serif",
})

# --- 2. FFmpeg 路徑設定 (請確認與您電腦的路徑一致) ---
ffmpeg_path = r"C:\Temp\ffmpeg-2026-05-21-git-0857141823-full_build\ffmpeg-2026-05-21-git-0857141823-full_build\bin\ffmpeg.exe"
if os.path.exists(ffmpeg_path):
    plt.rcParams['animation.ffmpeg_path'] = ffmpeg_path

# --- 3. 參數設定 (提速版本) ---
duration_seconds = 10  # 縮短到 10 秒，節奏更快
fps = 60
total_frames = duration_seconds * fps
num_particles = 50000 

plt.style.use('dark_background')
fig = plt.figure(figsize=(5.4, 9.6), facecolor='black')

# 繪圖區域配置
ax = fig.add_axes([0, 0.15, 1, 0.65]) 
ax.set_facecolor('black')
ax.set_aspect('equal')
ax.axis('off')

# --- 4. 文字顯示 ---
fig.text(0.5, 0.93, r"$\mathrm{CLIFFORD\ ATTRACTOR}$", ha='center', 
         color='white', fontsize=20, fontweight='bold', alpha=0.9)

formula_str = (r"$x_{n+1} = \sin(a y_n) + c \cos(a x_n)$" + "\n" + 
               r"$y_{n+1} = \sin(b x_n) + d \cos(b y_n)$")
formula_label = fig.text(0.5, 0.86, formula_str, ha='center', va='center', 
                         color='#00FFFF', fontsize=15, linespacing=1.6)

param_label = fig.text(0.5, 0.08, '', ha='center', color='white', 
                       fontsize=12, family='monospace', alpha=0.5)

# --- 5. 初始化繪圖物件 ---
scat = ax.scatter([], [], s=0.04, color='#00FFFF', alpha=0.4, edgecolors='none')
scat.set_clip_on(False) # 防止邊緣被切平

# --- 6. 核心計算函數 ---
def get_attractor_points(a, b, c, d, n):
    x, y = np.zeros(n), np.zeros(n)
    curr_x, curr_y = 0.1, 0.1 
    for i in range(n):
        next_x = np.sin(a * curr_y) + c * np.cos(a * curr_x)
        next_y = np.sin(b * curr_x) + d * np.cos(b * curr_y)
        x[i], y[i] = next_x, next_y
        curr_x, curr_y = next_x, next_y
    return x, y

# --- 7. 動畫更新函數 (提速邏輯) ---
def update(frame):
    progress = frame / (total_frames - 1)
    
    # 這裡的角速度 2*np.pi 保證了 10 秒內剛好完成一個完美循環 (Seamless Loop)
    angle = progress * 2 * np.pi
    
    # 稍微調大參數振幅，讓圖形「甩」動的幅度更大
    a = 1.6 + np.sin(angle) * 0.9
    b = 1.5 + np.cos(angle) * 1.0
    c = 1.4 + np.sin(angle * 1.5) * 0.7
    d = 1.6 + np.cos(angle) * 0.8
    
    x, y = get_attractor_points(a, b, c, d, num_particles)
    scat.set_offsets(np.c_[x, y])
    
    # 色彩變化速度也隨之加快
    color_val = plt.cm.cool(progress)
    scat.set_color(color_val)
    formula_label.set_color(color_val)
    
    # 動態視野跟隨
    margin = 0.2
    limit_x = (1 + abs(c)) + margin
    limit_y = (1 + abs(d)) + margin
    ax.set_xlim(-limit_x, limit_x)
    ax.set_ylim(-limit_y, limit_y) 
    
    param_label.set_text(f"a:{a:.2f}  b:{b:.2f}  c:{c:.2f}  d:{d:.2f}")
    
    return [scat, param_label]

# 建立動畫
my_animation = animation.FuncAnimation(
    fig, update, frames=total_frames, blit=False, interval=1000/fps, repeat=True
)

# =====================================================================
# ▼▼▼ 下載區塊 (直接在 plt.show 前執行) ▼▼▼
# =====================================================================
print("正在壓製 10 秒極速版數位絲綢影片...")
my_animation.save("clifford_fast_pro.mp4", fps=fps, dpi=200, 
                extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-b:v', '18M'])

plt.show()