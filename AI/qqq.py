import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

# 設定支持中文的字體
rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # Windows 常用字體
rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

# 加載數據
city_data_path = 'CITYData.csv'  # 請確認檔案路徑
taipei_data_path = 'Taipei.csv'  # 請確認檔案路徑

city_data = pd.read_csv(city_data_path)
taipei_data = pd.read_csv(taipei_data_path)

# 確保 'Statistical Period' 欄位為字串格式
city_data['Statistical Period'] = city_data['Statistical Period'].astype(str)

# 數據清理和日期格式處理
city_data = city_data.melt(id_vars='Statistical Period', var_name='District', value_name='EV_Count')
city_data['Year'] = city_data['Statistical Period'].str[:3].astype(int) + 1911  # 轉為西元年
city_data['Month'] = city_data['Statistical Period'].str[3:].astype(int)
city_data['Date'] = pd.to_datetime(city_data[['Year', 'Month']].assign(Day=1))
city_data = city_data.drop(columns=['Statistical Period', 'Year', 'Month'])

# 分組分析各區歷史電動車數量
district_trends = city_data.groupby(['Date', 'District'])['EV_Count'].sum().reset_index()
ev_summary = district_trends.groupby('District')['EV_Count'].sum().reset_index()

# 加載並分析充電站數據
station_summary = taipei_data.groupby('dist').size().reset_index(name='Station_Count')
merged_data = ev_summary.merge(station_summary, left_on='District', right_on='dist', how='left').fillna(0)

# 計算每站服務車輛數量
merged_data['Cars_per_Station'] = merged_data['EV_Count'] / merged_data['Station_Count']

# 設定每站服務車輛門檻並生成建議
threshold = 20000
merged_data['Recommendation'] = merged_data['Cars_per_Station'].apply(
    lambda x: '增設充電站' if x > threshold else '充電站足夠'
)

# 可視化每站服務車輛數量
plt.figure(figsize=(10, 6))
plt.bar(merged_data['District'], merged_data['Cars_per_Station'], color='skyblue', label='每站服務車輛數')
plt.axhline(y=threshold, color='r', linestyle='--', label='門檻 (20,000 車/站)')
plt.xticks(rotation=45)
plt.title('各行政區每站服務車輛數量')
plt.xlabel('行政區')
plt.ylabel('每站服務車輛數')
plt.legend()
plt.tight_layout()
plt.show()
