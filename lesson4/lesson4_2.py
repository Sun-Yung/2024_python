import tkinter as tk

def main():
    root = tk.Tk()
    print(type(root))
    root.title("我的第一個視窗")
    root.geometry("600x400")
    message=tk.Label(root,text="HELLO,我的一個視窗")
    message.pack()
    root.mainloop()

if __name__ =="__main__":
    main()