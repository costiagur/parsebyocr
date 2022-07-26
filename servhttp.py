import webserv
import webbrowser
import os
from sys import argv
import random
import ctypes
from myfunc import myfunc
import common

def main():

    common.intiate()

    try:

        HOST = '127.0.0.1'
        iniPORT = 50000
        newPORT = random.randint(50000,60000)
        CODESTR = "invoicebyocr"
        isrepliyed = 0

        print(argv)

        if len(argv) == 1:
            querystr = 'null'
        else:
            arglist = []

            for eacharg in argv[1:]:
                argarr = eacharg.split(":")
                arglist.append('"' + str(argarr[0]) + '":"' + str(argarr[1]) + '"')
            #

            querystr = "{" + ",".join(arglist) + "}"
        #

        currentfolder =  os.path.dirname(os.path.realpath(__file__))

        ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 0)

        htmlfilepath = "file://" + currentfolder + "/index.html"

        webbrowser.open(htmlfilepath) #open html file of the UI

        serv = webserv.HttpServer((HOST,iniPORT),webserv.Handler,CODESTR,newPORT,myfunc,querystr)

        while isrepliyed == 0:
            isrepliyed = serv.run_once()
        #

        serv.close()
        serv = webserv.HttpServer((HOST,newPORT),webserv.Handler,'',newPORT,myfunc,querystr)
        serv.run_continuously()

    except Exception as e:
        common.errormsg("Main",e)

    finally:
        common.root.destroy()

    common.root.mainloop()
 #

if __name__ == "__main__":
    main()
#