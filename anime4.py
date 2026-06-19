import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import os

# --- 1. 設置 LaTeX 字體 ---
plt.rcParams.update({
    "mathtext.fontset": "cm",
    "font.family": "serif",
})

# --- FFmpeg 路徑設定 ---
ffmpeg_path = r"C:\Temp\ffmpeg-2026-05-21-git-0857141823-full_build\ffmpeg-2026-05-21-git-0857141823-full_build\bin\ffmpeg.exe"
if os.path.exists(ffmpeg_path):
    plt.rcParams['animation.ffmpeg_path'] = ffmpeg_path

# --- 2. 準備質數數據 ---
def get_primes(n_limit):
    primes = []
    is_prime = [True] * (n_limit + 1)
    for p in range(2, n_limit + 1):
        if is_prime[p]:
            primes.append(p)
            for i in range(p * p, n_limit + 1, p):
                is_prime[i] = False
    return np.array(primes)

# 增加粒子到 20000 個，確保高倍率縮放後依然有細節
num_stars = 20000
primes = get_primes(300000)[:num_stars]

# --- 3. 參數與畫布設定 ---
duration_seconds = 15
fps = 60
total_frames = duration_seconds * fps

plt.style.use('dark_background')
fig = plt.figure(figsize=(5.4, 9.6), facecolor='black')
ax = fig.add_axes([0, 0, 1, 1]) 
ax.set_facecolor('black')
ax.set_aspect('equal')
ax.axis('off')

# --- 4. 還原經典開場文字 (0.15 比例) ---
text_elements = []
t1 = fig.text(0.5, 0.55, r"$\mathrm{THE\ PRIME\ GALAXY}$", ha='center', va='center', 
              color='white', fontsize=26, fontweight='bold', alpha=0)
t2 = fig.text(0.5, 0.48, r"$P_n = (p_n, p_n)$", ha='center', va='center', 
              color='#00FFCC', fontsize=22, alpha=0)
t3 = fig.text(0.5, 0.42, r"$\mathrm{Cosmic\ Order\ Revealed}$", ha='center', va='center', 
              color='white', fontsize=12, alpha=0)
text_elements = [t1, t2, t3]

# --- 5. 初始化繪圖物件 ---
star_cloud = ax.scatter([], [], s=1.0, edgecolors='none', color='#00FFCC', alpha=0)

# --- 6. 動畫更新函數 ---
def update(frame):
    progress = frame / (total_frames - 1)
    
    # --- 階段 A: 恢復經典文字閃現時間 (前 15%) ---
    if progress < 0.15:
        text_alpha = np.sin(progress / 0.15 * np.pi)
        for t in text_elements: t.set_alpha(text_alpha)
        star_alpha = progress / 0.15 * 0.4
    else:
        for t in text_elements: t.set_alpha(0)
        star_alpha = 1.0

    # --- 階段 B: 核心動力學 (旋轉加速) ---
    # 旋轉速度隨 progress 加快
    rot_speed_factor = 2 * np.pi + (progress ** 1.5) * 12 * np.pi
    rotation_offset = (frame / fps) * rot_speed_factor
    
    r = primes
    theta = primes + rotation_offset
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    
    star_cloud.set_offsets(np.c_[x, y])
    star_cloud.set_alpha(star_alpha)
    
    # --- 階段 C: 【核心修改】即時起跑的加速縮放 ---
    # 使用 1.5 次方曲線，這比 5 次方在開頭快得多，但結尾依然有衝刺感
    zoom_curve = np.power(progress, 1.5) 
    
    start_view = 600    # 中心特寫
    end_view = 200000   # 最終視野
    view_limit = start_view + (end_view - start_view) * zoom_curve
    
    # 設定 9:16 視野
    ax.set_xlim(-view_limit * 0.55, view_limit * 0.55)
    ax.set_ylim(-view_limit * 1.0, view_limit * 1.0) 
    
    # 顏色隨 progress 演變
    color_val = plt.cm.winter(0.2 + 0.8 * progress)
    star_cloud.set_color(color_val)
    
    return [star_cloud] + text_elements

# 建立動畫
my_animation = animation.FuncAnimation(
    fig, update, frames=total_frames, blit=False, interval=1000/fps, repeat=True
)

# =====================================================================
# ▼▼▼ 預覽視窗 ▼▼▼
print("正在壓製經典開場+即時加速版『質數星系』...")
output_name = "prime_galaxy_balanced_acceleration.mp4"
try:
    my_animation.save(
        output_name, 
        fps=fps, 
        dpi=200, 
        extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-b:v', '15M'],
        progress_callback=lambda i, n: print(f'渲染進度: {i+1}/{n}', end='\r')
    )
    print(f"\n儲存成功！檔案名稱：{output_name}")
except Exception as e:
    print(f"\n儲存失敗: {e}")
# =====================================================================
plt.show()