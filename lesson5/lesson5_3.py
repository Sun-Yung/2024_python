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
        ttk.Label(topFrame,text='是否同意',style='TopFrame.TLabel').pack()
        topFrame.pack(padx=20,pady=20)
        
        #==============end topFrame===============

        #==============bottomFrame===============
        bottomFrame = ttk.Frame(self)
        agreement = tk.StringVar()
        def agreement_changed():
            tk.messagebox.showinfo(title='Result',message=agreement.get())
        ttk.Checkbutton(bottomFrame,
            text='I agree',
            command=agreement_changed,
            variable=agreement,
            onvalue='agree',
            offvalue='disagree').pack()
        

        
        bottomFrame.pack(expand=True,fill='x',padx=20,pady=(0,20),ipadx=10,ipady=10)
        #==============end bottomFrame===============
    
    
        
def main():
    window = Window(theme="arc")
    window.mainloop()

if __name__ == '__main__':
    main()