import numpy as np
import matplotlib.pyplot as plt

# 1. 設定參數 - 增加點數讓表面更平滑
a = 1.0  
num_points = 200  # 從 100 提高到 200，畫面會細緻很多

def f(x):
    return 1 + np.sqrt(x) * np.exp(x**2)

# 2. 準備數據
x_vals = np.linspace(0, a, num_points)
theta = np.linspace(0, 2 * np.pi, num_points)
X, Theta = np.meshgrid(x_vals, theta)

# 計算半徑 r(x)
R = np.sqrt(X) * np.exp(X**2)

# 旋轉後的座標
Y = 1 + R * np.cos(Theta)
Z = R * np.sin(Theta)

# 3. 繪圖設定
# figsize 放大，並設定 layout 為 tight
fig = plt.figure(figsize=(12, 8)) 

# 創建 3D 子圖
ax = fig.add_subplot(111, projection='3d')

# 繪製表面
# cmap='magma' 或 'viridis' 顏色很漂亮
# antialiased=True 讓線條不破碎
surf = ax.plot_surface(X, Y, Z, cmap='magma', 
                       antialiased=True, 
                       alpha=0.9,
                       rcount=num_points, 
                       ccount=num_points)

# 繪製中心旋轉軸 (y=1)
ax.plot([0, a], [1, 1], [0, 0], color='cyan', lw=3, label='Axis y=1', zorder=10)

# 調整外觀
ax.set_title("Smoother 3D Solid of Revolution", fontsize=15)
ax.set_xlabel("X (Length)")
ax.set_ylabel("Y (Width)")
ax.set_zlabel("Z (Height)")

# 讓座標軸比例相等，這會讓圖形看起來不扁塌 (這在某些 Matplotlib 版本中很重要)
ax.set_box_aspect([1.5, 1, 1]) 

# 讓圖表預設放大一點
plt.subplots_adjust(left=0, right=1, bottom=0, top=1)

# 加入顏色條
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)

plt.show()