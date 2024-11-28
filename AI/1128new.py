import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns

# 設置支持中文的字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 微軟正黑體
plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

# 讀取數據
data_path = 'Latest_Data_For_Modeling.csv'  # 請將此文件名替換為您的 CSV 文件
data = pd.read_csv(data_path)

# 定義特徵與目標變數
X = data[['電動機車數量', '充電站數量', '每站服務車輛數', '人口密度']]
y = data['未來每站服務車輛數']

# 分割數據集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 初始化隨機森林模型
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)

# 使用交叉驗證評估模型性能
scores = cross_val_score(rf_model, X, y, cv=5, scoring='neg_mean_squared_error')
rmse_scores = (-scores) ** 0.5
average_rmse = rmse_scores.mean()
print(f"隨機森林模型的交叉驗證平均 RMSE：{average_rmse:.2f}")

# 訓練模型並進行測試集預測
rf_model.fit(X_train, y_train)
y_pred = rf_model.predict(X_test)

# 計算測試集的 MSE
mse = mean_squared_error(y_test, y_pred)
print(f"隨機森林模型的測試集均方誤差 (MSE): {mse:.2f}")

# 在完整數據集上進行預測
data['預測未來每站服務車輛數'] = rf_model.predict(X)

# 基於預測結果給出建議
def decision_rule(row):
    if row['預測未來每站服務車輛數'] > 3000:
        return '增設'
    elif row['預測未來每站服務車輛數'] < 1000:
        return '減少'
    else:
        return '維持不變'

data['建議'] = data.apply(decision_rule, axis=1)

# 保存結果到 CSV
output_path = 'RandomForest_Results.csv'
data.to_csv(output_path, index=False)
print(f"結果已保存至：{output_path}")





# 篩選數值列
numeric_columns = data.select_dtypes(include='number').columns

# 繪製合成圖表
plt.figure(figsize=(15, 10))
for idx, column in enumerate(numeric_columns, 1):
    plt.subplot(2, (len(numeric_columns) + 1) // 2, idx)
    sns.boxplot(data=data, y=column)
    plt.title(f'{column} 的分佈', fontsize=12)
    plt.ylabel(column, fontsize=10)
    plt.xticks([])  # 隱藏 x 軸標籤
    plt.tight_layout()

# 圖表總標題
plt.suptitle('所有數值列的盒鬚圖', fontsize=16, y=1.02)
plt.tight_layout()
plt.show()





# 繪製特徵重要性圖表
feature_importances = rf_model.feature_importances_
features = X.columns

plt.figure(figsize=(10, 6))
plt.barh(features, feature_importances)
plt.xlabel('特徵重要性', fontsize=12)
plt.ylabel('特徵名稱', fontsize=12)
plt.title('隨機森林模型的特徵重要性', fontsize=16)
plt.tight_layout()
plt.show()

# 繪製預測值與實際值對比圖表
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.7, label='預測值')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2, label='理想值（實際值=預測值）')
plt.xlabel('實際值', fontsize=12)
plt.ylabel('預測值', fontsize=12)
plt.title('測試集預測值與實際值對比', fontsize=16)
plt.legend(fontsize=12)
plt.tight_layout()
plt.show()

# 繪製各行政區的建議情況
plt.figure(figsize=(12, 8))
sns.barplot(data=data, x='行政區', y='預測未來每站服務車輛數', hue='建議', palette='Set2')
plt.title('各行政區充電站規劃建議', fontsize=16)
plt.xlabel('行政區', fontsize=12)
plt.ylabel('預測未來每站服務車輛數', fontsize=12)
plt.xticks(rotation=45)
plt.legend(title='建議', fontsize=10)
plt.tight_layout()
plt.show()