import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error

# 1. 讀取數據
latest_data_path = 'last.csv'  # 最新數據檔案
latest_data = pd.read_csv(latest_data_path)

# 2. 移除不必要的欄位（如索引列）
latest_data_cleaned = latest_data.drop(columns=['Unnamed: 0'])

# 3. 定義特徵與目標變數
X_latest = latest_data_cleaned[['電動機車數量', '充電站數量', '每站服務車輛數', '人口密度']]  # 特徵變數
y_latest = latest_data_cleaned['未來每站服務車輛數']  # 目標變數

# 4. 分割數據集
X_train_latest, X_test_latest, y_train_latest, y_test_latest = train_test_split(
    X_latest, y_latest, test_size=0.2, random_state=42)

# 5. 初始化隨機森林模型
rf_model_latest = RandomForestRegressor(n_estimators=100, random_state=42)

# 6. 使用交叉驗證評估模型性能
scores_latest = cross_val_score(rf_model_latest, X_latest, y_latest, cv=5, scoring='neg_mean_squared_error')
rmse_scores_latest = (-scores_latest) ** 0.5
average_rmse_latest = rmse_scores_latest.mean()
print(f"隨機森林模型的交叉驗證平均 RMSE：{average_rmse_latest:.2f}")

# 7. 訓練模型並進行測試集預測
rf_model_latest.fit(X_train_latest, y_train_latest)
y_pred_latest = rf_model_latest.predict(X_test_latest)

# 8. 計算測試集 MSE
mse_latest = mean_squared_error(y_test_latest, y_pred_latest)
print(f"隨機森林模型的測試集均方誤差 (MSE): {mse_latest:.2f}")

# 9. 在完整數據集上進行預測
latest_data_cleaned['預測未來每站服務車輛數'] = rf_model_latest.predict(X_latest)

# 10. 基於預測結果給出建議
def decision_rule_latest(row):
    if row['預測未來每站服務車輛數'] > 3000:
        return '增設'
    elif row['預測未來每站服務車輛數'] < 1000:
        return '減少'
    else:
        return '維持不變'

latest_data_cleaned['建議'] = latest_data_cleaned.apply(decision_rule_latest, axis=1)

# 11. 將結果保存為 CSV 文件
output_path_latest = r'C:\Users\user\Documents\data\test.csv'
latest_data_cleaned.to_csv(output_path_latest, index=False)
print(f"結果已保存至：{output_path_latest}")
