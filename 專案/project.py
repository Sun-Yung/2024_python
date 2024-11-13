
import pandas as pd
from tkinter import ttk
import tkinter as tk
from ttkthemes import ThemedTk
from tkinter.messagebox import showinfo

class Window(ThemedTk):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('登入')
        #==============style===============
        style = ttk.Style(self)
        style.configure('TopFrame.TLabel',font=('Helvetica',20))
        #============end style===============
        
        #==============top Frame===============

        topFrame = ttk.Frame(self)
        ttk.Label(topFrame,text='電動機車充電站查詢',style='TopFrame.TLabel').pack()
        topFrame.pack(padx=20,pady=20)
        
        #==============end topFrame===============

        #==============bottomFrame===============
        bottomFrame = ttk.Frame(self)
       
        self.selected_site = tk.StringVar()
        sitenames_cb = ttk.Combobox(bottomFrame, textvariable=self.selected_site,)
        self.selected_site.set('請選擇站點')
        sitenames_cb.pack(side='left',expand=True,anchor='n')        
        

        # define columns
        columns = ('sitename', 'address', 'city','dist')
    
        tree = ttk.Treeview(bottomFrame, columns=columns, show='headings')

        # define headings
        tree.heading('sitename', text='站點名稱')
        tree.heading('address', text='地址')
        tree.heading('city', text='縣市')
        tree.heading('dist', text='鄉鎮區')

        tree.column('sitename', width=150,anchor="center")
        tree.column('address', width=80,anchor="center")
        tree.column('city', width=80,anchor="center")
        tree.column('dist', width=50,anchor="center")

        # generate sample data
     
        tree.pack(side='right')
        bottomFrame.pack(expand=True,fill='x',padx=20,pady=(0,20),ipadx=10,ipady=10)

            #==============end bottomFrame===============
        
        def agreement_changed(self):
            showinfo(
                title='Agreement',
                message= self.agreement.get()

            )
    
    
        

def main():
    window = Window(theme="arc")
    window.mainloop()

if __name__ == '__main__':
    main()