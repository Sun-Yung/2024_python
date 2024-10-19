from ttkthemes import ThemedTk
from tkinter import ttk

class Window(ThemedTk):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.title('孫榕陽的lesson4作業')
        style = ttk.Style(self)        
        frame_width = 200
        # 上部按鈕區域
        topFrame = ttk.Frame(self,width=frame_width, borderwidth=1, relief='groove')

        btn1 = ttk.Button(topFrame, text="按鈕1")
        btn1.pack(side='left',fill='x', padx=10,pady=5)
        btn2 = ttk.Button(topFrame, text="按鈕2")
        btn2.pack(side='left', fill='x', padx=30,pady=5)
        btn3 = ttk.Button(topFrame, text="按鈕3")
        btn3.pack(side='left', fill='x', padx=10,pady=5)
        topFrame.pack(side="top",expand=True,padx=10, pady=10,fill='both')

        # 左邊按鈕區域
        leftFrame = ttk.Frame(self, width=frame_width, borderwidth=1, relief='groove')
        
        btn4 = ttk.Button(leftFrame, text="按鈕4")
        btn4.pack(side='top',expand=True,fill='both',padx=10,pady=5,ipady=30)
        btn5 = ttk.Button(leftFrame, text="按鈕5")
        btn5.pack(side='top',expand=True,fill='both',padx=10,pady=5,ipady=10)
        btn6 = ttk.Button(leftFrame, text="按鈕6")
        btn6.pack(side='top',expand=True,fill='both',padx=10,pady=5,ipady=10)
        leftFrame.pack(side='left', padx=10, pady=10, fill='both', expand=True)

        # 中間按鈕區域
        centerFrame = ttk.Frame(self, width=frame_width, borderwidth=1, relief='groove')
        
        btn7 = ttk.Button(centerFrame, text="按鈕7")
        btn7.pack(side='top',expand=True,fill='both',padx=10,pady=5,ipady=30)
        btn8 = ttk.Button(centerFrame, text="按鈕8")
        btn8.pack(side='top',expand=True,fill='both',padx=10,pady=5,ipady=10)
        btn9 = ttk.Button(centerFrame, text="按鈕9")
        btn9.pack(side='top',expand=True,fill='both',padx=10,pady=5,ipady=30)
        centerFrame.pack(side="left", padx=10, pady=10,fill='both', expand=True)

        # 右邊按鈕區域
        rightFrame = ttk.Frame(self, width=frame_width, borderwidth=1, relief='groove')
        
        btn10 = ttk.Button(rightFrame, text="按鈕10")
        btn10.pack(side='top',expand=True,fill='both',padx=10,pady=5,ipady=20)
        btn11 = ttk.Button(rightFrame, text="按鈕11")
        btn11.pack(side='top',expand=True,fill='both',padx=10,pady=5,ipady=20)
        btn12 = ttk.Button(rightFrame, text="按鈕12")
        btn12.pack(side='top',expand=True,fill='both',padx=10,pady=5,ipady=20)
        rightFrame.pack(side="left", padx=10, pady=10,fill='both', expand=True)



def main():
    window = Window(theme="arc")
    window.mainloop()

if __name__ == '__main__':
    main()
