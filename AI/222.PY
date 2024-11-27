import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 設定支持中文的字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 適用於 Windows
plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

# 加載數據
city_data_path = 'CITYData.csv'
taipei_data_path = 'Taipei.csv'

city_data = pd.read_csv(city_data_path)
taipei_data = pd.read_csv(taipei_data_path)

# 數據清理與整合
city_data_long = city_data.melt(id_vars='Statistical Period', 
                                var_name='行政區', 
                                value_name='電動機車數量')

city_data_long['Year'] = city_data_long['Statistical Period'].astype(str).str[:3].astype(int) + 1911
city_data_long['Month'] = city_data_long['Statistical Period'].astype(str).str[3:].astype(int)

# 修正日期處理，添加 Day=1 並確保類型正確
city_data_long['Date'] = pd.to_datetime(city_data_long[['Year', 'Month']].assign(Day=1))

city_data_long = city_data_long.drop(columns=['Statistical Period', 'Year', 'Month'])

charging_station_summary = taipei_data.groupby('dist').size().reset_index(name='充電站數量')
charging_station_summary.rename(columns={'dist': '行政區'}, inplace=True)

merged_data = city_data_long.groupby('行政區')['電動機車數量'].max().reset_index()
merged_data = merged_data.merge(charging_station_summary, on='行政區', how='left').fillna(0)

# 計算特徵
merged_data['每站服務車輛數'] = merged_data['電動機車數量'] / merged_data['充電站數量'].replace(0, 1)
merged_data['未來車輛數量'] = merged_data['電動機車數量'] * 1.1  # 假設10%增長
merged_data['未來每站服務車輛數'] = merged_data['未來車輛數量'] / merged_data['充電站數量'].replace(0, 1)

merged_data['地區類型'] = np.random.choice(['市區', '郊區', '鄉村'], size=len(merged_data))

# 分類邏輯
def classify_decision(row):
    if row['地區類型'] == '市區':
        if row['未來每站服務車輛數'] > 3000:
            return '增設'
        elif row['未來每站服務車輛數'] < 1000:
            return '減少'
        else:
            return '維持不變'
    elif row['地區類型'] == '郊區':
        if row['未來每站服務車輛數'] > 2500:
            return '增設'
        elif row['未來每站服務車輛數'] < 800:
            return '減少'
        else:
            return '維持不變'
    else:  # 鄉村
        if row['未來每站服務車輛數'] > 2000:
            return '增設'
        elif row['未來每站服務車輛數'] < 500:
            return '減少'
        else:
            return '維持不變'

merged_data['建議'] = merged_data.apply(classify_decision, axis=1)

# 輸出結果表格
print("行政區充電站建議表：")
print(merged_data[['行政區', '電動機車數量', '充電站數量', '每站服務車輛數', '建議']])

# 條形圖：每個區域的建議
plt.figure(figsize=(12, 8))
sns.barplot(data=merged_data, x='行政區', y='未來每站服務車輛數', hue='建議', palette='coolwarm')
plt.title('各行政區充電站建議', fontsize=16)
plt.xlabel('行政區', fontsize=14)
plt.ylabel('未來每站服務車輛數', fontsize=14)
plt.xticks(rotation=45)
plt.legend(title='建議', loc='upper right')
plt.tight_layout()
plt.show()
