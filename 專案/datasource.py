import sqlite3
import pandas as pd
import csv
# 1. 讀取 CSV 檔案
csv_file = './battery01.csv'  # 替換成你的 CSV 檔案路徑
df = pd.read_csv(csv_file)

# 2. 連接到 SQLite 資料庫（如果資料庫不存在，它會自動創建）
conn = sqlite3.connect('example.db')  # 替換成你的資料庫檔案
cursor = conn.cursor()

# 3. 創建資料表（如果需要的話）
# 假設你的 CSV 檔案包含欄位 "id", "name", "age"
# 這裡會根據 CSV 的列自動創建相應的表格

table_name = "battery"
create_table_query = """
CREATE TABLE IF NOT EXISTS battery (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER
)
"""
cursor.execute(create_table_query)

# 4. 將 CSV 資料插入資料庫
df.to_sql(table_name, conn, if_exists='replace', index=False)

# 5. 提交並關閉連線
conn.commit()
conn.close()

print(f"資料已經成功從 '{csv_file}' 插入到資料庫中。")
#---------------------------------------------------------------------------------

import requests
import sqlite3
def get_sitename(county:str)->list[str]:
    '''
    docString
    parameter:
        county:城市名稱
    return:
        傳出所有的站點名稱
    '''
    conn = sqlite3.connect("example.db")
    with conn:
        cursor = conn.cursor()
        sql = '''
        SELECT DISTINCT sitename
        FROM battery
        WHERE county=?
        '''
        cursor.execute(sql,(county,))
        city = [items[0] for items in cursor.fetchall()]
    
    return city

def get_county()->list[str]:
    '''
    docString
    parameter:
    return:
        傳出所有的城市名稱
    '''
    conn = sqlite3.connect("example.db")
    with conn:
        # Create a cursor object to execute SQL commands
        cursor = conn.cursor()
        # SQL query to select unique sitenames from records table
        sql = '''
        SELECT DISTINCT county
        FROM battery
        '''
        # Execute the SQL query
        cursor.execute(sql)
        # Get all results and extract first item from each row into a list
        dist = [items[0] for items in cursor.fetchall()]
    
    # Return the list of unique sitenames
    return dist

    
def get_selected_data(city:str)->list[list]:
    '''
    使用者選擇了sitename,並將sitename傳入
    Parameter:
        sitename: 站點的名稱
    Return:
        所有關於此站點的相關資料
    '''
    conn=sqlite3.connect("AQI.db")
    with conn:
        cursor=conn.cursor()
        sql='''
        SELECT date,county,sitename,aqi,pm25,status,lat,lon
        FROM battery
        WHERE sitename=?
        ORDER BY date DESC;
        '''
        cursor.execute(sql,(city,))
        sitename_list=[list(item)for item in cursor.fetchall()]
        return sitename_list
import sqlite3
import csv

def download_data():
    try:
        # 讀取 CSV 檔案
        with open("battery01.csv", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)  # 使用 DictReader 來讀取 CSV 內容

            # 連接到 SQLite 資料庫
            conn = sqlite3.connect("example.db")
            cursor = conn.cursor()

            # 逐行讀取 CSV 資料並插入資料庫
            for row in csv_reader:
                # 假設 CSV 有欄位 sitename, city, dist, address
                sitename = row['sitename']
                city = row['city']
                dist = row['dist']
                address = row['address']

                sql = '''
                INSERT OR IGNORE INTO records (sitename, city, dist, address)
                VALUES (?, ?, ?, ?);
                '''
                cursor.execute(sql, (sitename, city, dist, address))

            # 提交並關閉連線
            conn.commit()
            conn.close()

        print("資料已經成功從 'battery.csv' 插入到資料庫中。")
    
    except Exception as e:
        print(f"發生錯誤: {e}")
