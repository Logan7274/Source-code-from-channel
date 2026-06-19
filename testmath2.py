import numpy as np
import plotly.graph_objects as go

# 1. 數據準備
a = 1.0
n = 100  # Plotly 處理 100 點非常輕鬆
x = np.linspace(0, a, n)
theta = np.linspace(0, 2*np.pi, n)
X, Theta = np.meshgrid(x, theta)

# 計算半徑 r(x) = sqrt(x) * e^(x^2)
R = np.sqrt(X) * np.exp(X**2)

# 旋轉座標 (繞 y=1 旋轉)
Y = 1 + R * np.cos(Theta)
Z = R * np.sin(Theta)

# 2. 建立 3D 表面
fig = go.Figure(data=[go.Surface(
    x=X, y=Y, z=Z, 
    colorscale='Magma', 
    colorbar_title='Radius',
    hovertemplate='x: %{x}<br>y: %{y}<br>z: %{z}<extra></extra>'
)])

# 3. 加入旋轉軸 (y=1 的那根紅線)
fig.add_trace(go.Scatter3d(
    x=[0, a], y=[1, 1], z=[0, 0],
    mode='lines',
    line=dict(color='cyan', width=6),
    name='Rotation Axis (y=1)'
))

# 4. 設定佈局
fig.update_layout(
    title='Interactive 3D Solid of Revolution (Super Smooth!)',
    scene=dict(
        xaxis_title='X (Length)',
        yaxis_title='Y (Width)',
        zaxis_title='Z (Height)',
        aspectmode='manual',
        aspectratio=dict(x=1.5, y=1, z=1), # 讓喇叭拉長一點好觀察
    ),
    margin=dict(l=0, r=0, b=0, t=40)
)

fig.show()