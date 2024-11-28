import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error

# 1. 讀取數據

# (a) 讀取最新的合併數據（含人口密度）
latest_data_path = 'last.csv'
latest_data = pd.read_csv(latest_data_path)

# (b) 讀取行政區面積數據
area_data = pd.DataFrame({
    '行政區': ['松山區', '信義區', '大安區', '中山區', '中正區', '大同區', '萬華區', '文山區',
             '南港區', '內湖區', '士林區', '北投區'],
    '面積': [9.2878, 11.2077, 11.3614, 13.6821, 7.6071, 5.6815, 8.8522, 31.509,
             21.8424, 31.5787, 62.3682, 56.8216]
})

# 2. 合併面積數據到最新數據
merged_data = pd.merge(latest_data, area_data, on='行政區', how='left')

# 3. 計算新特徵
merged_data['每平方公里電動機車數量'] = merged_data['電動機車數量'] / merged_data['面積']
merged_data['每平方公里充電站數量'] = merged_data['充電站數量'] / merged_data['面積']

# 4. 移除不必要的索引欄位
merged_data_cleaned = merged_data.drop(columns=['Unnamed: 0.1', 'Unnamed: 0'], errors='ignore')

# 5. 定義特徵與目標變數
X = merged_data_cleaned[['電動機車數量', '充電站數量', '每站服務車輛數', '人口密度', '每平方公里電動機車數量', '每平方公里充電站數量']]
y = merged_data_cleaned['未來每站服務車輛數']

# 6. 分割數據集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 7. 初始化隨機森林模型
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)

# 8. 使用交叉驗證評估模型性能
scores = cross_val_score(rf_model, X, y, cv=5, scoring='neg_mean_squared_error')
rmse_scores = (-scores) ** 0.5
average_rmse = rmse_scores.mean()
print(f"隨機森林模型的交叉驗證平均 RMSE：{average_rmse:.2f}")

# 9. 訓練模型並進行測試集預測
rf_model.fit(X_train, y_train)
y_pred = rf_model.predict(X_test)

# 10. 計算測試集的 MSE
mse = mean_squared_error(y_test, y_pred)
print(f"隨機森林模型的測試集均方誤差 (MSE): {mse:.2f}")

# 11. 在完整數據集上進行預測
merged_data_cleaned['預測未來每站服務車輛數'] = rf_model.predict(X)

# 12. 基於預測結果給出建議
def decision_rule(row):
    if row['預測未來每站服務車輛數'] > 3000:
        return '增設'
    elif row['預測未來每站服務車輛數'] < 1000:
        return '減少'
    else:
        return '維持不變'

merged_data_cleaned['建議'] = merged_data_cleaned.apply(decision_rule, axis=1)



# 13. 將結果保存為 CSV 文件
output_path = r'C:\Users\user\Documents\data\new.csv'
merged_data_cleaned.to_csv(output_path, index=False)
print(f"結果已保存至：{output_path}")

