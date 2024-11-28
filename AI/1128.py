import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# 1. 讀取處理後的數據
file_path = 'FeatureData.csv'  # 替換為您的檔案路徑
data = pd.read_csv(file_path)

# 2. 特徵與目標變數
X = data[['電動機車數量', '充電站數量', '每站服務車輛數']]  # 特徵變數
y = data['未來每站服務車輛數']  # 目標變數

# 3. 分割數據集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. 初始化隨機森林模型
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)

# 5. 使用交叉驗證評估模型性能
scores = cross_val_score(rf_model, X, y, cv=5, scoring='neg_mean_squared_error')
rmse_scores = (-scores) ** 0.5
average_rmse = rmse_scores.mean()
print(f"隨機森林模型的交叉驗證平均 RMSE：{average_rmse:.2f}")

# 6. 訓練模型並進行測試集預測
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)

# 7. 計算測試集 MSE
mse_rf = mean_squared_error(y_test, y_pred_rf)
print(f"隨機森林模型的測試集均方誤差 (MSE): {mse_rf:.2f}")

# 8. 在完整數據集上進行預測
data['預測未來每站服務車輛數'] = rf_model.predict(X)

# 9. 基於預測結果給出建議
def decision_rule(row):
    if row['預測未來每站服務車輛數'] > 3000:  # 門檻值可以調整
        return '增設'
    elif row['預測未來每站服務車輛數'] < 1000:
        return '減少'
    else:
        return '維持不變'

data['建議'] = data.apply(decision_rule, axis=1)

# 10. 將結果保存為 CSV 文件
output_path = r'C:\Users\user\Documents\data\1128.csv'
data.to_csv(output_path, index=False)
print(f"結果已保存至：{output_path}")
