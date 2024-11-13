
import datasource

from tkinter import ttk
import tkinter as tk
from ttkthemes import ThemedTk
from tkinter.messagebox import showinfo
import view

class Window(ThemedTk):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('登入')
        self.resizable(False,False)
        #==============style===============
        style = ttk.Style(self)
        style.configure('TopFrame.TLabel',font=('Helvetica',20))
        #============end style===============
        
        #==============top Frame===============

        topFrame = ttk.Frame(self)
        ttk.Label(topFrame,text='空氣品質指標(AQI)(歷史資料)',style='TopFrame.TLabel').pack()
        topFrame.pack(padx=20,pady=20)
        
        #==============end topFrame===============

        #==============bottomFrame===============
        bottomFrame = ttk.Frame(self,padding=[10,10,10,10])
            #==============selectedFrame===============
        self.selectedframe=ttk.Frame(self,padding=[10,10,10,10])
        #增加refresh按鈕
       
        icon_button=view.Imagebutton(self.selectedframe,command=lambda:datasource.download_data())
        icon_button.pack()


        #============combobox選擇城市
        counties = datasource.get_county()
        # self.selected_site = tk.StringVar()
        self.selected_county=tk.StringVar()
        sitenames_cb = ttk.Combobox(self.selectedframe, textvariable=self.selected_county,values=counties,state='readonly')
        self.selected_county.set('請選擇城市')
        sitenames_cb.bind('<<ComboboxSelected>>', self.county_selected)
        sitenames_cb.pack(anchor='n')

        self.sitenameFrame=None

        self.selectedframe.pack(side="left",fill="y")    
            #==============end selectedFrame===============
        
        #=====rightframe===============
        rightframe=ttk.LabelFrame(bottomFrame,text="站點資訊",padding=[10,10,10,10])
        #建立treeview
        # define columns
        columns = ('date', 'county',"sitename" ,'aqi', 'pm25','status','lat','lon')

        self.tree = ttk.Treeview(rightframe, columns=columns, show='headings')
        self.tree.bind('<<TreeviewSelect>>', self.item_selected)
        # define headings
        self.tree.heading('date', text='日期')
        self.tree.heading('county', text='縣市')
        self.tree.heading('sitename', text='站點')
        self.tree.heading('aqi', text='AQI')
        self.tree.heading('pm25', text='PM25')
        self.tree.heading('status',text='狀態')
        self.tree.heading('lat', text='緯度')
        self.tree.heading('lon', text='經度')

        self.tree.column('date', width=150,anchor="center")
        self.tree.column('county', width=80,anchor="center")
        self.tree.column('sitename', width=80,anchor="center")
        self.tree.column('aqi', width=50,anchor="center")
        self.tree.column('pm25', width=50,anchor="center")
        self.tree.column('status', width=50,anchor="center")
        self.tree.column('lat', width=100,anchor="center")
        self.tree.column('lon', width=100,anchor="center")
        
        
        self.tree.pack(side='right')

        rightframe.pack(side="right")


        #=====end rightframe===========



        
        bottomFrame.pack()

            #==============end bottomFrame===============
    def county_selected(self,event):
        selected=self.selected_county.get()
        sitenames=datasource.get_sitename(county=selected)
        #listbox選擇站點
        if self.sitenameFrame:
            self.sitenameFrame.destroy()

        self.sitenameFrame=view.SitenameFrame(master=self.selectedframe,sitenames=sitenames,radio_controll=self.radio_button_click)
        self.sitenameFrame.pack()

    
    def radio_button_click(self,         selected_sitename:str):
        '''
        - 此method是傳遞給SitenameFrame實體
        - 當sitenameFrame內的radiobutton被選取時,會連動執行此method
        Parameter:
            selected_sitename:str -> 這是被選取的站點名稱
        '''
        for children in self.tree.get_children():
            self.tree.delete(children)
        selected_data=datasource.get_selected_data(selected_sitename)
        for record in selected_data:
            self.tree.insert("", "end", values=record)

     
    def item_selected(self,event):
        for selected_item in self.tree.selection():
            record = self.tree.item(selected_item)
            dialog=view.MycustomDialog(parent=self,title=f'{record["values"][1]}-{record["values"][2]}',record=record['values'])

def main():
    datasource.download_data() #下載至資料庫
    window = Window(theme="arc")
    window.mainloop()

if __name__ == '__main__':
    main()
