import tkinter as tk
from tkinter import ttk
from tkintermapview import TkinterMapView
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import matplotlib

# 設置 Matplotlib 字體以支持中文
matplotlib.rc("font", family="Microsoft JhengHei")  # 使用微軟正黑體
plt.rcParams["axes.unicode_minus"] = False  # 防止負號顯示錯誤

# 讀取數據
data_path = 'Latest_Data_For_Modeling.csv'  # 替換為你的數據檔案
map_data_path = 'taipeimap.csv'  # 替換為包含經緯度的檔案路徑

data = pd.read_csv(data_path)
map_data = pd.read_csv(map_data_path)

# 定義特徵與目標變數
X = data[['電動機車數量', '充電站數量', '每站服務車輛數', '人口密度']]
y = data['未來每站服務車輛數']

# 分割數據集並訓練模型
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# 預測並生成建議
data['預測未來每站服務車輛數'] = rf_model.predict(X)
def decision_rule(row):
    if row['預測未來每站服務車輛數'] > 3000:
        return '增設'
    elif row['預測未來每站服務車輛數'] < 1000:
        return '減少'
    else:
        return '維持不變'
data['建議'] = data.apply(decision_rule, axis=1)

# 初始化主視窗
root = tk.Tk()
root.title("充電站規劃建議")
root.geometry("1200x700")

# 左側框架
left_frame = tk.Frame(root, width=300, bg="lightgray", padx=10, pady=10)
left_frame.pack(side=tk.LEFT, fill=tk.Y)

# 地圖框架
map_widget = TkinterMapView(root, width=600, height=400, corner_radius=0)
map_widget.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
map_widget.set_position(25.0330, 121.5654)  # 預設台北市位置
map_widget.set_zoom(12)

# 按鈕 - 顯示盒鬚圖
def show_boxplot():
    numeric_columns = data.select_dtypes(include='number').columns
    fig, axes = plt.subplots(2, (len(numeric_columns) + 1) // 2, figsize=(8, 6))
    axes = axes.ravel()
    for idx, column in enumerate(numeric_columns):
        sns.boxplot(data=data, y=column, ax=axes[idx])
        axes[idx].set_title(f'{column} 的分佈')
    for ax in axes[len(numeric_columns):]:
        ax.remove()
    fig.tight_layout()
    plt.show()

btn_boxplot = tk.Button(left_frame, text="顯示盒鬚圖", command=show_boxplot)
btn_boxplot.pack(pady=5)

# 按鈕 - 顯示特徵重要性
def show_feature_importance():
    feature_importances = rf_model.feature_importances_
    features = X.columns

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(features, feature_importances, color="skyblue")
    ax.set_title("特徵重要性", fontsize=16)
    ax.set_xlabel("重要性", fontsize=12)
    ax.set_ylabel("特徵名稱", fontsize=12)
    plt.tight_layout()
    plt.show()

btn_feature_importance = tk.Button(left_frame, text="顯示特徵重要性", command=show_feature_importance)
btn_feature_importance.pack(pady=5)

# 按鈕 - 顯示全局分析結果
def show_global_analysis():
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(
        data=data,
        x="行政區",
        y="預測未來每站服務車輛數",
        hue="建議",
        palette="Set2",
        ax=ax
    )
    ax.set_title("各行政區充電站規劃建議", fontsize=16)
    ax.set_xlabel("行政區", fontsize=12)
    ax.set_ylabel("預測未來每站服務車輛數", fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

btn_global_analysis = tk.Button(left_frame, text="顯示分析結果", command=show_global_analysis)
btn_global_analysis.pack(pady=5)

# 標題 - 選擇行政區
admin_area_label = tk.Label(left_frame, text="選擇行政區", bg="lightgray")
admin_area_label.pack(anchor="w")

admin_areas = list(map_data['dist'].unique())  # 獲取行政區列表
admin_area_combo = ttk.Combobox(left_frame, values=admin_areas, state="readonly")
admin_area_combo.pack(fill=tk.X, pady=5)

# 分析結果區域
result_frame = tk.Frame(left_frame)
result_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10, anchor="s")

# 顯示行政區分析結果的圖表
def update_analysis_plot(selected_area):
    for widget in result_frame.winfo_children():
        widget.destroy()  # 清除舊圖表

    filtered_data = data[data['行政區'] == selected_area]
    if filtered_data.empty:
        tk.Label(result_frame, text="該行政區無分析數據").pack()
        return

     # 繪製分析結果棒狀圖
    fig, ax = plt.subplots(figsize=(2.5, 5))  # 調整圖表大小
    sns.barplot(
        data=filtered_data,
        x="建議",
        y="預測未來每站服務車輛數",
        palette="Set2",
        ax=ax
    )
    ax.set_title(f"{selected_area} 分析結果", fontsize=10)
    ax.set_xlabel("建議", fontsize=8)
    ax.set_ylabel("預測未來每站服務車輛數", fontsize=8)
    ax.set_ylim(0, 1000)  # 限制 Y 軸範圍
    ax.tick_params(axis='x', labelsize=8)
    ax.tick_params(axis='y', labelsize=8)
    fig.tight_layout()

    # 在 Tkinter 視窗中嵌入圖表
    canvas = FigureCanvasTkAgg(fig, result_frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()

# 根據選擇的行政區顯示地圖標記並更新分析結果
def show_district_markers(event=None):
    selected_area = admin_area_combo.get()
    if selected_area:
        map_widget.delete_all_marker()
        filtered_data = map_data[map_data['dist'] == selected_area]
        
        if not filtered_data.empty:
            # 計算行政區的中心位置和範圍
            center_lat = filtered_data['lat'].mean()
            center_lon = filtered_data['lon'].mean()
            
            # 設置地圖位置到該行政區中心
            map_widget.set_position(center_lat, center_lon)
            map_widget.set_zoom(14)  # 調整縮放等級
            
            # 添加地圖標記
            for _, row in filtered_data.iterrows():
                lat, lon = row['lat'], row['lon']
                sitename = row['sitename']
                map_widget.set_marker(lat, lon, text=sitename)
        else:
            tk.messagebox.showwarning("提示", f"行政區 {selected_area} 沒有充電站數據！")

        # 更新分析結果
        update_analysis_plot(selected_area)
    else:
        tk.messagebox.showwarning("提示", "請先選擇行政區！")

admin_area_combo.bind("<<ComboboxSelected>>", show_district_markers)

# 啟動主視窗
root.mainloop()
