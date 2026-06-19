import matplotlib.pyplot as plt
import numpy as np

# 設定畫布風格
plt.style.use('seaborn-v0_8-whitegrid')

# 準備數據 (Block Model Waste Rock in Million Tonnes)
deposits = ['Deposit 1\n(Underground)', 'Deposit 2\n(Deep Pit)', 'Deposit 3\n(Shallow Pit)']
waste_vol = [29.6, 314.7, 77.5] 
# Dep 1: 29,565,000 -> 29.6M
# Dep 2: 314,685,000 -> 314.7M
# Dep 3: 77,490,000 -> 77.5M

# 顏色邏輯：
# Deposit 2 廢石爆量 -> 紅色 (危險)
# Deposit 3 我們的選擇 -> 綠色
# Deposit 1 -> 灰色 (雖然少但不是重點)
colors = ['#95a5a6', '#c0392b', '#27ae60'] 

# 建立畫布
fig, ax = plt.subplots(figsize=(7, 5))

# 繪製長條圖
bars = ax.bar(deposits, waste_vol, color=colors, width=0.6)

# 在柱子上標示數據
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 5,
            f'{height} M', ha='center', va='bottom', fontsize=14, fontweight='bold')

# 設定標題與軸標籤
ax.set_ylabel('Waste Rock (Million Tonnes)', fontsize=12, fontweight='bold')
ax.set_title('Environmental Burden: Waste Generation', fontsize=15, fontweight='bold', pad=15)
ax.set_ylim(0, 360) # 留點空間給標籤
ax.grid(axis='x')

plt.tight_layout()
plt.show()
# plt.savefig('waste_3_compare.png', dpi=300)