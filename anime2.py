import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from numpy import sin, cos

# --- 【FFmpeg 路徑設定】 ---
plt.rcParams['animation.ffmpeg_path'] = r"C:\Temp\ffmpeg-2026-05-21-git-0857141823-full_build\ffmpeg-2026-05-21-git-0857141823-full_build\bin\ffmpeg.exe"

# --- 1. 物理與模擬參數 ---
num_pendulums = 60      
duration_seconds = 10    
fps = 60
total_frames = duration_seconds * fps
dt = 1.0 / fps

L1, L2 = 1.0, 1.0       
M1, M2 = 1.0, 1.0       
G = 12.0                

th1_init = np.pi / 1.5   
th2_init = np.pi / 2    
epsilon = 0.02          

# --- 2. 物理方程式 (RK4) ---
def get_derivs(state):
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
    k1 = get_derivs(state)
    k2 = get_derivs(state + 0.5 * dt * k1)
    k3 = get_derivs(state + 0.5 * dt * k2)
    k4 = get_derivs(state + dt * k3)
    return state + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

# --- 3. 預計算 ---
print("正在模擬系統...")
all_x1 = np.zeros((num_pendulums, total_frames))
all_y1 = np.zeros((num_pendulums, total_frames))
all_x2 = np.zeros((num_pendulums, total_frames))
all_y2 = np.zeros((num_pendulums, total_frames))

for i in range(num_pendulums):
    state = np.array([th1_init, 0.0, th2_init + i * epsilon, 0.0])
    for f in range(total_frames):
        t1, w1, t2, w2 = state
        all_x1[i, f] = L1 * sin(t1)
        all_y1[i, f] = -L1 * cos(t1)
        all_x2[i, f] = all_x1[i, f] + L2 * sin(t2)
        all_y2[i, f] = all_y1[i, f] - L2 * cos(t2)
        state = rk4_step(state, dt)

# --- 4. 動畫畫面設定 ---
fig = plt.figure(figsize=(5.4, 9.6), facecolor='black')
# 調整繪圖區域，為頂部公式留出空間
ax = fig.add_axes([0, 0, 1, 0.8]) 
ax.set_xlim(-2.3, 2.2)
ax.set_ylim(-3.0, 1.5)
ax.set_aspect('equal')
ax.axis('off')

# --- 【新增】標題與公式文字 ---
fig.text(0.5, 0.94, "CHAOS: DOUBLE PENDULUM", ha='center', color='white', fontsize=18, fontweight='bold')

# 使用 LaTeX 格式顯示物理公式
formula_text = (
    r"$x_1 = L_1 \sin \theta_1, \quad y_1 = -L_1 \cos \theta_1$" + "\n"
    r"$x_2 = x_1 + L_2 \sin \theta_2, \quad y_2 = y_1 - L_2 \cos \theta_2$" + "\n"
    r"$\mathcal{L} = T - V \quad \text{(Lagrangian dynamics)}$"
)
fig.text(0.5, 0.84, formula_text, ha='center', color='#00FFCC', fontsize=11, linespacing=1.8, alpha=0.9)

# 顯示初始微差參數
fig.text(0.5, 0.81, rf"$\Delta \theta_0 = {epsilon}$ ", ha='center', color='white', fontsize=10, alpha=0.6)

colors = plt.cm.turbo(np.linspace(0, 1, num_pendulums))

lines = [ax.plot([], [], color=colors[i], lw=2, alpha=0.9)[0] for i in range(num_pendulums)]
trails = [ax.plot([], [], color=colors[i], lw=1, alpha=0.4)[0] for i in range(num_pendulums)]
points = [ax.plot([], [], 'o', color=colors[i], markersize=5)[0] for i in range(num_pendulums)]

# --- 5. 動畫更新函數 ---
def update(frame):
    trail_len = 45 
    start = max(0, frame - trail_len)
    for i in range(num_pendulums):
        x1, y1 = all_x1[i, frame], all_y1[i, frame]
        x2, y2 = all_x2[i, frame], all_y2[i, frame]
        lines[i].set_data([0, x1, x2], [0, y1, y2])
        points[i].set_data([x2], [y2])
        trails[i].set_data(all_x2[i, start:frame+1], all_y2[i, start:frame+1])
    return lines + points + trails

my_animation = animation.FuncAnimation(
    fig, update, frames=total_frames, blit=True, interval=1000/fps
)

# =====================================================================
# ▼▼▼ 下載區塊貼在下面 ▼▼▼
# ---【獨立的儲存區塊】---
print("正在壓製帶有公式的混沌動畫...")
my_animation.save(
    "chaos_formula_shorts.mp4", 
    fps=fps, 
    dpi=300,
    extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p'],
    progress_callback=lambda i, n: print(f'進度: {i+1}/{n}', end='\r')
)
print("\n儲存成功：chaos_formula_shorts.mp4")

# =====================================================================

plt.show()