import tkinter

infoobj = ''

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

class infopopup:
    def __init__(self,parent):
        self.top = tkinter.Toplevel(parent)
        self.top.attributes("-topmost", 1)
        self.lab = tkinter.Label(self.top,text = '')
        self.lab.pack()
    #

    def show(self,newtext):
        self.lab['text'] = self.lab['text'] + "\n" + newtext
        self.lab.update()
    #        

    def close(self):
        self.top.destroy()
    #
#