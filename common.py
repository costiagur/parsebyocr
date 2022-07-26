import tkinter

def intiate():
    global root
    root = tkinter.Tk()
    root.attributes("-topmost", 1)
    root.withdraw()
#

def errormsg(title,message):
    root.deiconify()
    tkinter.messagebox.showerror(title=title, message=message)
    root.withdraw()
#
      