import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import os

# --- 1. 環境設定 ---
ffmpeg_path = r"C:\Temp\ffmpeg-2026-05-21-git-0857141823-full_build\ffmpeg-2026-05-21-git-0857141823-full_build\bin\ffmpeg.exe"
if os.path.exists(ffmpeg_path):
    plt.rcParams['animation.ffmpeg_path'] = ffmpeg_path

# --- 2. 動畫與高解析度參數 ---
duration_seconds = 15
fps = 60
total_frames = duration_seconds * fps

# 大幅提升網格解析度 (320x180)，使細節更精緻
rows, cols = 320, 180 

# --- 3. 畫布設定 (標準 9:16 全螢幕) ---
plt.style.use('dark_background')
fig = plt.figure(figsize=(5.4, 9.6), facecolor='black')
# 佔滿整個視窗，不留任何邊距
ax = fig.add_axes([0, 0, 1, 1])
ax.axis('off')

# 使用 'inferno' 色圖，色彩跨度更廣，質感更高級
img = ax.imshow(np.zeros((rows, cols)), cmap='inferno', interpolation='nearest', vmin=0, vmax=1)

# --- 4. 3D 投影邏輯 ---
def rotate_cube(points, A, B, C):
    """三維旋轉矩陣運算"""
    rx = np.array([[1, 0, 0],
                   [0, np.cos(A), -np.sin(A)],
                   [0, np.sin(A), np.cos(A)]])
    ry = np.array([[np.cos(B), 0, np.sin(B)],
                   [0, 1, 0],
                   [-np.sin(B), 0, np.cos(B)]])
    rz = np.array([[np.cos(C), -np.sin(C), 0],
                   [np.sin(C), np.cos(C), 0],
                   [0, 0, 1]])
    return points @ rx.T @ ry.T @ rz.T

def get_high_res_cube(width):
    """生成極高密度的立方體表面點雲"""
    res = 45 # 提升單邊密度，確保旋轉時表面無空隙
    p = np.linspace(-width, width, res)
    x, y, z = np.meshgrid(p, p, p)
    mask = (np.abs(x) == width) | (np.abs(y) == width) | (np.abs(z) == width)
    return np.vstack([x[mask], y[mask], z[mask]]).T

# 生成三層嵌套立方體
cube_sizes = [20, 12, 6]
base_points = [get_high_res_cube(s) for s in cube_sizes]

# --- 5. 核心渲染循環 ---
def update(frame):
    progress = frame / (total_frames - 1)
    
    # 建立空的螢幕緩衝區與深度緩衝區
    buffer = np.zeros((rows, cols))
    z_buffer = np.full((rows, cols), -1e10)
    
    # 指數級旋轉加速度
    A = progress * 6 * np.pi + (progress**2.2) * 4 * np.pi
    B = progress * 4 * np.pi + (progress**1.8) * 3 * np.pi
    C = progress * 3 * np.pi
    
    # 指數級拉遠運鏡 (Zoom Out)
    dist_base = 55
    distance = dist_base + (progress**2) * 180
    
    # 投影焦距
    K1 = 260 

    for i, p_cloud in enumerate(base_points):
        # 不同層級採用不同旋轉偏好
        rotated = rotate_cube(p_cloud, A * (1 + i*0.05), B * (1 - i*0.05), C)
        
        # 透視投影轉換
        z_coords = rotated[:, 2] + distance
        ooz = 1.0 / z_coords # 深度倒數
        
        # 投影至 2D 網格
        xp = (cols / 2 + (K1 * ooz * rotated[:, 0])).astype(int)
        yp = (rows / 2 + (K1 * ooz * rotated[:, 1])).astype(int)
        
        # 根據深度設定亮度強度
        intensity = 0.35 + (i * 0.25)
        
        # Z-Buffer 遮擋測試
        for j in range(len(xp)):
            if 0 <= xp[j] < cols and 0 <= yp[j] < rows:
                if ooz[j] > z_buffer[yp[j], xp[j]]:
                    z_buffer[yp[j], xp[j]] = ooz[j]
                    buffer[yp[j], xp[j]] = intensity

    # 極微弱的掃描線特效 (增加數位感但不破壞清晰度)
    buffer[::3, :] *= 0.9 
    
    img.set_data(buffer)
    return [img]

# --- 6. 建立動畫物件 ---
my_animation = animation.FuncAnimation(
    fig, update, frames=total_frames, blit=True, interval=1000/fps
)

# =====================================================================
# ---【獨立儲存區塊：壓製極致高清 1080x1920 影片】---
# =====================================================================
print("正在以最高規格壓製影片...")
output_name = "pure_ascii_cube_ultra_hd.mp4"

try:
    my_animation.save(
        output_name, 
        fps=fps, 
        dpi=300,        # 300 DPI 確保點陣極其銳利
        extra_args=[
            '-vcodec', 'libx264', 
            '-pix_fmt', 'yuv420p', 
            '-b:v', '20M',     # 超高碼率 (20Mbps) 杜絕任何方塊雜訊
            '-profile:v', 'high', 
            '-level', '4.2'
        ],
        progress_callback=lambda i, n: print(f'渲染進度: {i+1}/{n} 影格', end='\r')
    )
    print(f"\n\n壓製完成！檔案：{output_name}")
except Exception as e:
    print(f"\n儲存錯誤: {e}")
print("正在啟動 3D 渲染引擎預覽 (無文字純淨版)...")
plt.show()