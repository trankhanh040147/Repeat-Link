from concurrent.futures import thread
from modulefinder import packagePathMap
from operator import truediv
import tkinter as tk
from tkinter import DISABLED, filedialog,Text
import os
from turtle import title
import webbrowser as wb #Open URL
import time
import threading

defaultConnectionLink = "http://10.15.99.1:1999/cgi-bin/authenticate?mac=14%3A13%3A33%3A0e%3A1f%3A39&redirect=https%3A%2F%2Ffptplay.vn%2F"
delayTimeReopen = 1 # (seconds): delay time when open the browser
delayTimeClose = 1 # (seconds): delay time when kill the process
delayBetweenWindows = 4 # (seconds): delay time when open more than 1 tab

defaultTimeClose = 2 # (seconds)
defaultTimeReopen = 15*60 - 20 # (seconds)
defaultTotalWindows = 1 

bg_default = "#262626"
bg_running = "#00e639"

def Run():
    #Gán giá trị biến Running
    global Running
    global timeReopen
    global timeClose
    global totalWindows
    global browser_1st

    def Get_Browser_Name(browser_dir):
        #Get the program's name from a directory |ex: Get_Browser_Name('..//brave.exe') --> 'brave.exe' | 
        return browser_dir[browser_dir.rfind("//")+2::]

    #Default 1st browser is assigned to Brave, if you haven't chosen any browser yet, it's will automatically assign to brave
    try:
        browser_1st
    except NameError:
         browser_1st = "C://Program Files//BraveSoftware//Brave-Browser//Application//brave.exe"

    if True:
        while Running:
            t=timeReopen
            timeReopen = float(enTimeReopen.get()) + delayTimeClose #Make for the 2nd time, like a do-while loop
            while t and Running:
                time.sleep(1)
                t-=1.0
            #If Stop button is pressed, kill this thread
            if not Running:
                return
            #open link using selected browsers
            windows = totalWindows
            while windows:
                wb.get('browser_1st').open(connectionLink.get())    
                time.sleep(delayBetweenWindows)
                windows -=1

            #close the browser after timeClose run out
            t_close = timeClose
            while t_close:
                time.sleep(1)
                t_close-=1.0
            os.system("taskkill /f /im "+Get_Browser_Name(browser_1st))

def Start_Command():
    global Running
    global timeReopen
    global timeClose
    global totalWindows
    global threadRun

    threadRun = threading.Thread(target=Run)
    
    # Get values from input
    timeReopen = 0 # Do once in the beginning then set the time re-open
    timeClose = float(enTimeClose.get()) +delayTimeReopen 
    totalWindows = float(enTotalWindows.get())
    
    #Default 1st browser is assigned to Brave, if you haven't chosen any browser yet, it's will automatically assign to brave
    try:
        browser_1st
    except NameError:
         browser_1st = "C://Program Files//BraveSoftware//Brave-Browser//Application//brave.exe"

    #Register các browser để sử dụng
    wb.register('browser_1st',None,
        wb.BackgroundBrowser(browser_1st)
    )
    
    btn_Start.config(bg=bg_running)
    Running = True
    threadRun.start()
    return

def Stop_Command():
    global Running
    Running = False
    btn_Start.config(bg=bg_default)
    return

def Select_File_1st():
        
    filetypes = (
        ('text files', '*.exe'),
        ('All files', '*.*')
    )

    #Must declare a global variable inside this function, otherwise it'll not work
    #Biến lưu trữ đường dẫn chứa browser đầu tiên
    global browser_1st 

    browser_1st = filedialog.askopenfilename(
        title ='Open a file',
        initialdir='/',
        filetypes=filetypes
    )
    browser_1st=browser_1st.replace('/','//')

    tk.messagebox.showinfo(
        title='Đã chọn trình duyệt',
        message=browser_1st
    )

    return browser_1st


if __name__ == "__main__":
    
    root = tk.Tk()
    root.geometry('350x200')
    root.title("Repeat link")
    root.eval('tk::PlaceWindow . center')

    #Các biến lưu giá trị 
    connectionLink = tk.StringVar()
    connectionLink.set(defaultConnectionLink)
    # timeReopen = 0 
    # timeClose = 0
    # totalWindows = 0

        #Biến lưu text cho entry
    txtTimeClose = tk.StringVar()
    txtTimeClose.set(defaultTimeClose)
    txtTimeReopen = tk.StringVar()
    txtTimeReopen.set(defaultTimeReopen)
    txtTotalWindows = tk.StringVar()
    txtTotalWindows.set(defaultTotalWindows)

    #biến lưu giá trị cho biết có đang chạy tính năng lặp hay không
    global Running
    Running = False

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # Textbox (Entry) chứa link 
    enConnection = tk.Entry(bd=3, width=150, textvariable=connectionLink)
    enConnection.pack()

    # Textbox (Entry) chứa thời gian đóng trang 
    enTimeClose = tk.Entry(bd=3, width=10, textvariable=txtTimeClose)
    enTimeClose.pack()

    # Textbox (Entry) chứa thời gian reset 
    enTimeReopen = tk.Entry(bd=3, width=10, textvariable=txtTimeReopen)
    enTimeReopen.pack()

    # Textbox (Entry) chứa tổng số cửa sổ sẽ mở 
    enTotalWindows = tk.Entry(bd=3, width=10, textvariable=txtTotalWindows)
    enTotalWindows.pack()
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    
    #Select Browser
    btn_OpenBrowser1st = tk.Button(root, text= 'Select browser',
                        command=Select_File_1st)
    btn_OpenBrowser1st.pack(expand=True)

    # Button start
    btn_Start = tk.Button(root, text="Start", padx=10, pady=5, fg = "white", bg=bg_default, 
                        command= Start_Command)
    btn_Start.pack()
        

    # Button stop
    btn_Stop = tk.Button(root, text="Stop", padx=10, pady=5, fg = "white", bg=bg_default, 
                        command= Stop_Command)
        #wait for the threadStop to terminate
    btn_Stop.pack()

    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    #Get current position ([x,y]) of objects
    # root.update()
    # print(f"Connection entry: {enConnection.winfo_rootx()},{enConnection.winfo_rooty()}")
    # print(f"TimeClose entry: {enTimeClose.winfo_rootx()},{enTimeClose.winfo_rooty()}")
    # print(f"TimeReOpen entry: {enTimeReopen.winfo_rootx()},{enTimeReopen.winfo_rooty()}")
    # print(f"TotalWindows entry: {enTotalWindows.winfo_rootx()},{enTotalWindows.winfo_rooty()}")

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #Các label hiện chú thích
    lbl_TimeClose = tk.Label(root, text ="Close browser after: ").place(x=18, y=22)
    lbl_TimeReopen = tk.Label(root, text ="Reopen the link every: ").place(x=18, y=45)
    lbl_TotalWindows = tk.Label(root, text ="Total tabs: ").place(x=18, y=68)
    lbl_TimeClose_unit = tk.Label(root, text="(seconds)").place(x=222, y=22)
    lbl_TimeReopen_unit = tk.Label(root, text="(seconds)").place(x=222, y=45)
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    root.mainloop()

    
