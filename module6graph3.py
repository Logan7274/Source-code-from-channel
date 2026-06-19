import matplotlib.pyplot as plt
import numpy as np

# 設定畫布風格
plt.style.use('seaborn-v0_8-whitegrid')

# 準備數據 (SLCA Health & Safety Total Score)
deposits = ['Deposit 1\n(Underground)', 'Deposit 2\n(Deep Pit)', 'Deposit 3\n(Shallow Pit)']
scores = [3, 8, 11]  # Dep 1=3, Dep 2=8, Dep 3=11
colors = ['#c0392b', '#f39c12', '#27ae60'] # 紅(危險) -> 橘(普通) -> 綠(最安全)

# 建立畫布
fig, ax = plt.subplots(figsize=(7, 5))

# 繪製長條圖
bars = ax.bar(deposits, scores, color=colors, width=0.6)

# 在柱子上標示分數
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.2,
            f'{int(height)}', ha='center', va='bottom', fontsize=14, fontweight='bold')

# 設定標題與軸標籤
ax.set_ylabel('SLCA Safety Score (Max 12)', fontsize=12, fontweight='bold')
ax.set_title('Worker Safety Comparison (Higher is Better)', fontsize=15, fontweight='bold', pad=15)
ax.set_ylim(0, 13)
ax.grid(axis='x') # 只顯示 Y 軸網格線

plt.tight_layout()
plt.show()
# plt.savefig('safety_3_compare.png', dpi=300)