import sqlite3
import pandas as pd
import csv
import requests
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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city,
    dist,
    sitename,
    address
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
        SELECT DISTINCT dist
        FROM battery
        WHERE city=?
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
        SELECT DISTINCT city
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
    conn=sqlite3.connect("example.db")
    with conn:
        cursor=conn.cursor()
        sql='''
        SELECT city,dist,Sitename,address
        FROM battery
        WHERE dist=?
        
        '''
        cursor.execute(sql,(city,))
        sitename_list=[list(item)for item in cursor.fetchall()]
        return sitename_list


def download_data():
    conn = sqlite3.connect("example.db")

    try:
        # 假設 CSV 檔案的路徑是 "battery.csv"
        csv_file = 'battery01.csv'  # 請替換成你的 CSV 檔案路徑
        df = pd.read_csv(csv_file)

    except FileNotFoundError as e:
        print(f"檔案未找到: {e}")
        return
    except pd.errors.EmptyDataError as e:
        print(f"CSV 檔案為空: {e}")
        return
    except Exception as e:
        print(f"讀取 CSV 發生錯誤: {e}")
        return
    else:
        # 假設 CSV 檔案有 'sitename', 'city', 'dist', 'address' 等欄位
        with conn:
            cursor = conn.cursor()

            for index, row in df.iterrows():
                city = row['city']
                dist = row['dist']
                sitename = row['sitename']
                address = row['address']

                # 檢查資料是否完整
                if not all([city, dist, sitename, address]):
                    print(f"跳過不完整的資料: {row}")
                    continue  # 跳過不完整的項目

                # 插入資料庫
                sql = '''INSERT OR IGNORE INTO battery(city, dist, sitename, address)
                         VALUES (?, ?, ?, ?)'''
                cursor.execute(sql, (city, dist, sitename, address))

        print("資料已成功下載並插入資料庫。")



