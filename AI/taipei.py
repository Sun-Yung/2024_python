import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
import matplotlib.font_manager as fm

# 設置中文字體，解決中文顯示問題
font_path = "C:/Windows/Fonts/simsun.ttc"  # 替換為您的系統中文字體路徑
font_prop = fm.FontProperties(fname=font_path)

# 讀取 Taipei.csv 文件
file_path = 'Taipei.csv'
taipei_data = pd.read_csv(file_path, encoding='utf-8-sig')

# 修正列名
taipei_data.columns = ['sitename', 'address', 'city', 'dist', 'lat', 'lon']

# 計算每個區域的充電站數量
charging_density = taipei_data.groupby('dist').size().reset_index(name='充電站數量')

# 繪製垂直條形圖
plt.figure(figsize=(12, 8))
plt.bar(charging_density['dist'], charging_density['充電站數量'], color='skyblue', alpha=0.8)
plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))  # 美化數字格式
plt.title("各區域充電站數量分佈", fontsize=16, fontproperties=font_prop)
plt.xlabel("區域", fontsize=14, fontproperties=font_prop)
plt.ylabel("充電站數量", fontsize=14, fontproperties=font_prop)
plt.xticks(rotation=45, fontsize=12, fontproperties=font_prop)  # 旋轉區域名稱
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 添加數據標籤
for i, value in enumerate(charging_density['充電站數量']):
    plt.text(i, value, str(value), ha='center', fontsize=10, fontproperties=font_prop)

plt.tight_layout()
plt.show()
