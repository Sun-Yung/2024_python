import tkinter as tk
from tkinter import ttk, messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# 建立 Selenium 瀏覽器啟動函數
def start_shopping():
    # 從輸入欄位中取得使用者資料
    email = entries["電郵"].get()
    password = entries["密碼"].get()
    product_name = entries["商品名稱"].get()
    product_size = entries["商品尺寸"].get()  # 取得商品尺寸
    card_number = entries["卡號"].get()
    card_holder = entries["持卡人"].get()
    expiry_date = entries["有效期限(MM/YY)"].get()
    cvv = entries["安全碼"].get()
    
    # 檢查輸入欄位是否填寫完整
    if not all([email, password, product_name, product_size, card_number, card_holder, expiry_date, cvv]):
        messagebox.showwarning("警告", "請完整填寫所有欄位")
        return
    
    # 開始自動購物
    try:
        driver_path = "chromedriver.exe"  # 替換成您的 ChromeDriver 路徑
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service)

        driver.get("https://www.goopi.co/")
        
        # 登入流程
        login_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "登入"))
        )
        login_button.click()
        
        email_input = driver.find_element(By.NAME, "email")
        email_input.send_keys(email)
        
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        
        # 搜尋商品
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.send_keys(product_name)
        search_box.send_keys(Keys.RETURN)
        
        # 選擇商品並加入購物車
        product_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, product_name))
        )
        product_link.click()

        # 選擇尺寸
        try:
            size_button = driver.find_element(By.XPATH, f"//button[text()='{product_size}']")
            size_button.click()
        except:
            print("找不到尺寸按鈕")

        # 加入購物車
        add_to_cart_button = driver.find_element(By.ID, "add_to_cart_button")
        add_to_cart_button.click()

        # 前往結帳
        checkout_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "結帳"))
        )
        checkout_button.click()

        # 填寫結帳資料
        driver.find_element(By.NAME, "card_number").send_keys(card_number)
        driver.find_element(By.NAME, "card_holder").send_keys(card_holder)
        driver.find_element(By.NAME, "expiry_date").send_keys(expiry_date)
        driver.find_element(By.NAME, "cvv").send_keys(cvv)

        # 提交訂單
        driver.find_element(By.ID, "submit_order").click()
        
        messagebox.showinfo("成功", "訂單提交成功！")
    except Exception as e:
        messagebox.showerror("錯誤", f"購物過程出錯: {e}")
    finally:
        time.sleep(5)
        driver.quit()

# 建立 tkinter 主視窗
root = tk.Tk()
root.title("機器人")
root.geometry("400x450")

# 設定標籤及輸入欄位
fields = ["電郵", "密碼", "商品名稱", "卡號", "持卡人", "有效期限(MM/YY)", "安全碼"]
entries = {}

for i, field in enumerate(fields):
    label = ttk.Label(root, text=field)
    label.grid(row=i, column=0, sticky="w", padx=10, pady=5)
    
    entry = ttk.Entry(root, width=30, show="*" if field == "密碼" else None)
    entry.grid(row=i, column=1, pady=5)
    entries[field] = entry

# 增加尺寸選單
size_label = ttk.Label(root, text="商品尺寸")
size_label.grid(row=len(fields), column=0, sticky="w", padx=10, pady=5)

size_var = tk.StringVar()
size_dropdown = ttk.Combobox(root, textvariable=size_var, values=["1", "2", "3", "4"])  # 假設尺寸有 S, M, L, XL
size_dropdown.grid(row=len(fields), column=1, pady=5)
size_dropdown.current(1)  # 預設選擇 M

entries["商品尺寸"] = size_dropdown

# 開始搶購按鈕
submit_button = ttk.Button(root, text="開始搶購吧！", command=start_shopping)
submit_button.grid(row=len(fields)+1, column=0, columnspan=2, pady=20)

# 啟動 tkinter 主迴圈
root.mainloop()


