import matplotlib.pyplot as plt
import numpy as np

# 設定畫布風格
plt.style.use('seaborn-v0_8-whitegrid')

# 準備數據 (WDM: Job and Business Opportunities)
deposits = ['Deposit 1\n(Remote)', 'Deposit 2\n(Moderate)', 'Deposit 3\n(Near Town)']
scores = [2, 5, 8]  # Dep 1=2, Dep 2=5, Dep 3=8
colors = ['#95a5a6', '#f39c12', '#27ae60'] # 灰(差) -> 橘(普通) -> 綠(最好)

# 建立畫布
fig, ax = plt.subplots(figsize=(7, 5))

# 繪製長條圖
bars = ax.bar(deposits, scores, color=colors, width=0.6)

# 在柱子上標示分數
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.2,
            f'{int(height)}/10', ha='center', va='bottom', fontsize=14, fontweight='bold')

# 設定標題與軸標籤
ax.set_ylabel('WDM Score (Local Jobs)', fontsize=12, fontweight='bold')
ax.set_title('Community Impact: Job & Business Opportunities', fontsize=15, fontweight='bold', pad=15)
ax.set_ylim(0, 10) # WDM 滿分是 10
ax.grid(axis='x')

plt.tight_layout()
plt.show()
# plt.savefig('jobs_comparison.png', dpi=300)