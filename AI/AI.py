import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller

# 加載數據
file_path = './AIdata.csv'  # 確認資料檔案路徑
data = pd.read_csv(file_path)

# 數據清理
if data['electric motorcycle'].dtype == 'object':
    data['electric motorcycle'] = data['electric motorcycle'].str.replace(',', '').astype(int)
if data['all'].dtype == 'object':
    data['all'] = data['all'].str.replace(',', '').astype(int)

data['year'] = data['month_range'].astype(str).str[:3].astype(int) + 1911  # 民國轉西元
data['month'] = data['month_range'].astype(str).str[3:].astype(int)
data['monthly_electric_increase'] = data['electric motorcycle'].diff().fillna(0)

# 加入日期作為 x 軸標籤
data['date'] = pd.to_datetime(data[['year', 'month']].assign(day=1))

# 提取時間序列
time_series = data['monthly_electric_increase']

# 平穩性檢測並進行差分（如必要）
adf_test = adfuller(time_series)
print("ADF Test Statistic:", adf_test[0])
print("p-value:", adf_test[1])

if adf_test[1] > 0.05:  # 如果 p-value > 0.05，時間序列需要進一步差分
    time_series = time_series.diff().dropna()

# 設置和訓練 ARIMA 模型
model = ARIMA(time_series, order=(1, 1, 1))  # 假設 (p=1, d=1, q=1)
fitted_model = model.fit()

# 預測未來 12 個月
forecast_steps = 12
future_forecast = fitted_model.forecast(steps=forecast_steps)

# 繪製歷史數據與預測結果
plt.figure(figsize=(12, 6))
plt.plot(data['date'], data['monthly_electric_increase'], label='Historical Data', marker='o', color='blue')
plt.plot(
    pd.date_range(start=data['date'].iloc[-1], periods=forecast_steps + 1, freq='M')[1:],  # 預測日期範圍
    future_forecast,
    label='Forecast',
    color='red',
    marker='x'
)
plt.title("ARIMA Model - Forecast for Next 12 Months", fontsize=14)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Monthly Increase in Registrations", fontsize=12)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.xticks(rotation=45)  # 調整 x 軸日期顯示角度
plt.show()

# 輸出未來 12 個月的預測結果
print("Future Forecast for Next 12 Months:")
print(future_forecast)
