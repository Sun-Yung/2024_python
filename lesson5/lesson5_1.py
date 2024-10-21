from tkinter import ttk
import tkinter as tk
from ttkthemes import ThemedTk
from tkinter.messagebox import showinfo

class Window(ThemedTk):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        #====================style================================
        style=ttk.Style(self)
        style.configure("topFrame.TLabel",font=("arial",20))
        #====================style,end============================

        #====================topframe=============================
        topFrame=ttk.Frame(self)
        ttk.Label(topFrame,text="個人資料輸入:",style="topFrame.TLabel").pack()
        topFrame.pack(padx=20,pady=20)
        #====================topframe,end=========================

        #====================bottomframe==========================
        bottomFrame=ttk.Frame(self)
        ttk.Label(bottomFrame,text="username:").grid(column=0,row=0,sticky="E")
        
        self.usename=tk.StringVar()
        ttk.Entry(bottomFrame,textvariable=self.usename).grid(column=1,row=0,pady=10)
        ttk.Label(bottomFrame,text="password:").grid(row=1,column=0,sticky="E")
        
        self.password=tk.StringVar()
        ttk.Entry(bottomFrame,textvariable=self.password,show="*").grid(column=1,row=1,padx=10,pady=10)

        cancel_btn=ttk.Button(bottomFrame,text="取消",command=self.cancel_click)
        cancel_btn.grid(column=0,row=2,padx=10,pady=(30,0))

        ok_btn=ttk.Button(bottomFrame,text="確認",command=self.ok_click)
        ok_btn.grid(column=1,row=2,padx=10,pady=(30,0),sticky="E")

        bottomFrame.pack(expand=True,fill="x",padx=20,pady=(0,20))
        #====================bottomframe,end======================
    def cancel_click(self):
        self.usename.set("")
        self.password.set("")

    def ok_click(self):
        username = self.usename.get()
        password = self.password.get()
        showinfo(title="使用者輸入",message=f'使用者名稱:{username}\n使用者密碼:{password}')





def main():
    window = Window(theme="arc")
    # window.usename.set("這裡放姓名")
    # window.password.set("這裡打密碼")
    window.mainloop()




if __name__ == '__main__':
    main()