from tkinter import ttk
import tkinter as tk
class SitenameFrame(ttk.Frame):#繼承
    '''
    SitenameFrame主要是提供一個自訂的frame,當使用者選取城市時必須要建立對應的sitenameframe
    sitenameframe內會使用checkbox_widget,提供給使用者會勾選那一個站點
    '''

    def __init__(self,master=None,sitenames:list[str]=[],radio_controll=None,**kwargs):
        self.radio_controll=radio_controll
        super().__init__(master=master,**kwargs)
        #欄寬
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.selected_radio=tk.StringVar()
        for idx,value in enumerate(sitenames):
            column=idx%2
            index=int(idx/2)
            print(idx,value)
            ttk.Radiobutton(self,
                            text=value,value=value,variable=self.selected_radio,
                            command=self.radio_button_selected).grid(column=column,row=index,sticky="w")

            print("========================")
    def radio_button_selected(self):
       if self.radio_controll != None:
           self.radio_controll(self.selected_radio.get())
