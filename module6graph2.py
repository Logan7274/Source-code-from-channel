import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 1. 設定畫布
fig, ax = plt.subplots(figsize=(14, 5))
ax.set_xlim(0, 16)
ax.set_ylim(0, 6)
ax.axis('off')  # 關閉座標軸

# 2. 定義步驟數據
steps = [
    {"title": "Block Modeling", "sub": "(Resource Estimation)", "color": "#2c3e50"}, # 深藍灰
    {"title": "SLCA", "sub": "(Life Cycle Assessment)", "color": "#27ae60"},         # 環保綠
    {"title": "System Resiliency", "sub": "(CLD & Risk)", "color": "#f39c12"},       # 警示橘
    {"title": "WDM", "sub": "(Final Recommendation)", "color": "#c0392b"}            # 決策紅
]

# 3. 定義方塊的位置參數
box_width = 3
box_height = 1.8
y_pos = 2.5
start_x = 1
gap = 4  # 每個方塊中心的間距

# 4. 繪製流程圖函數
for i, step in enumerate(steps):
    # 計算方塊中心點
    x_center = start_x + i * gap
    
    # (A) 畫圓角矩形 (Box)
    # xy 是左下角座標，所以要扣掉寬高的一半
    rect = patches.FancyBboxPatch(
        (x_center - box_width/2, y_pos - box_height/2),
        box_width, box_height,
        boxstyle="round,pad=0.2,rounding_size=0.2",
        linewidth=2,
        edgecolor=step['color'],
        facecolor='white', # 內部留白，看起來比較清新
        zorder=2
    )
    ax.add_patch(rect)
    
    # (B) 畫上方色塊 (Header) 讓它看起來像卡片
    # 這是一個純裝飾，讓標題有背景色
    header = patches.FancyBboxPatch(
        (x_center - box_width/2, y_pos),
        box_width, box_height/2, # 只蓋上半部
        boxstyle="round,pad=0.2,rounding_size=0.2",
        linewidth=0,
        edgecolor='none',
        facecolor=step['color'],
        alpha=0.1, # 淡色背景
        zorder=1
    )
    ax.add_patch(header)

    # (C) 加入文字 (Text)
    # 主標題
    ax.text(x_center, y_pos + 0.3, step['title'], 
            ha='center', va='center', fontsize=14, fontweight='bold', color=step['color'])
    # 副標題
    ax.text(x_center, y_pos - 0.4, step['sub'], 
            ha='center', va='center', fontsize=11, style='italic', color='#555555')

    # (D) 畫箭頭 (Arrow) - 除了最後一個步驟外，都要畫指向下一個的箭頭
    if i < len(steps) - 1:
        arrow_start = x_center + box_width/2 + 0.2
        arrow_end = (start_x + (i+1) * gap) - box_width/2 - 0.2
        
        arrow = patches.FancyArrowPatch(
            (arrow_start, y_pos), 
            (arrow_end, y_pos),
            arrowstyle='-|>', 
            mutation_scale=20, # 箭頭大小
            color='#95a5a6',
            linewidth=2
        )
        ax.add_patch(arrow)

# 5. 加入總標題
plt.title("Engineering Evaluation Process: A Holistic Approach", fontsize=18, weight='bold', pad=20, color='#333333')

# 6. 顯示圖表
plt.tight_layout()
plt.show()
# plt.savefig('process_flow.png', dpi=300) # 若要存檔請取消註解