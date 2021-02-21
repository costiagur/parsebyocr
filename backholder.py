import tkinter
import tkinter.ttk

def holderrun(naming="UIhtml"):

    global root

    root = tkinter.Tk()

    root.title(naming)

    frame = tkinter.ttk.Frame(root,padding=(12,12,12,12))
    frame.grid(column=0, row=0)
    tkinter.ttk.Label(frame,text="Running " + naming).grid(column=1,row=1)

    root.mainloop() #holds server from going to shutdown in the next command
#

def holderclose():
    root.destroy()
#
