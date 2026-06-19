import matplotlib.pyplot as plt

# 1. 數據準備 (來自你的 WDM 表格)
labels = [
    'Expected Profit (25%)', 
    'Impact on Environment (20%)', 
    'Safety (20%)', 
    'Resiliency of Mine System (15%)', 
    'Indigenous Lifestyle (10%)', 
    'Local Jobs & Business (10%)'
]

sizes = [25, 20, 20, 15, 10, 10]

# 2. 顏色設定 (專業工程配色)
# Profit: 金色/黃色
# Environment/Safety/Resiliency: 藍綠色系 (代表安全與永續)
# Social: 暖色系/紫色
colors = ['#f4c542', '#2E8B57', '#4682B4', '#5F9EA0', '#DA70D6', '#FF7F50']

# 3. 繪製圓餅圖
fig, ax = plt.subplots(figsize=(10, 7))

# explode 用來將 "Profit" 稍微分離出來，或者把 "Environment" 分離出來
# 這裡我們讓所有區塊緊密結合，看起來比較整體
explode = (0.05, 0, 0, 0, 0, 0)  

wedges, texts, autotexts = ax.pie(sizes, 
                                  explode=explode, 
                                  labels=labels, 
                                  colors=colors, 
                                  autopct='%1.1f%%', # 顯示百分比
                                  startangle=140,    # 旋轉角度，讓大塊的在上面
                                  pctdistance=0.85,  # 百分比距離圓心的距離
                                  textprops={'fontsize': 20, 'weight': 'bold'} # 文字大小
                                 )

# 4. 畫一個白色的圓圈在中間 (變成甜甜圈圖 Donut Chart，看起來比較現代專業)
centre_circle = plt.Circle((0,0),0.70,fc='white')
fig.gca().add_artist(centre_circle)

# 5. 中間加上標題文字
ax.text(0, 0, 'Decision\nWeighting', horizontalalignment='center', verticalalignment='center', fontsize=16, fontweight='bold', color='#333333')

# 6. 設定標題與樣式
ax.axis('equal')  # 確保圓形不變形
plt.title('WDM Criteria Weighting Distribution', fontsize=18, pad=20)
plt.tight_layout()

# 7. 顯示或存檔
plt.show()
# plt.savefig('wdm_chart.png', dpi=300) # 如果要存檔把這行註解拿掉