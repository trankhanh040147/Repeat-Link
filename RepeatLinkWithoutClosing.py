from concurrent.futures import thread
from faulthandler import disable
from modulefinder import packagePathMap
from operator import truediv
import tkinter as tk
from tkinter import DISABLED, filedialog,Text
import os
import webbrowser as wb #Open URL
import time
import threading

defaultConnectionLink1 = "https://dkmh.hcmute.edu.vn/DangKiNgoaiKeHoach/DanhSachLopHocPhan/221LLCT120405?CurriculumID=LLCT120405&t=0.29671356313722086"
defaultConnectionLink2 = "https://dkmh.hcmute.edu.vn/DangKiNgoaiKeHoach/DanhSachLopHocPhan/221SOEN330679?CurriculumID=SOEN330679&t=0.16596112049962297"
defaultConnectionLink3 = "https://dkmh.hcmute.edu.vn/DangKiNgoaiKeHoach/DanhSachLopHocPhan/221PHED130715?CurriculumID=PHED130715&t=0.5963126691157028"
defaultBrowser = "C://Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"

delayTimeReopen = 1 # (seconds): delay time when open the browser

delayBetweenWindows = 4 # (seconds): delay time when open more than 1 tab
delayTimeBetweenLinks = 7 # (seconds): time open the links after another


defaultTimeReopen = 15*60 # (seconds)
defaultTotalWindows = 1 

bg_default = "#262626"
bg_running = "#00e639"

def Run():
    #Gán giá trị biến Running
    global Running
    global timeReopen
    global timeClose
    global totalWindows

    def Get_Browser_Name(browser_dir):
        #Get the program's name from a directory |ex: Get_Browser_Name('..//brave.exe') --> 'brave.exe' | 
        return browser_dir[browser_dir.rfind("//")+2::]

    if True:
        while Running:
            t=timeReopen
            timeReopen = float(enTimeReopen.get())  #Make for the 2nd time, like a do-while loop
            while t and Running:
                time.sleep(1)
                t-=1.0
            #If Stop button is pressed, kill this thread
            if not Running:
                return
            #open link using selected browsers
            windows = totalWindows
            while windows:
                wb.get('browser_1st').open(connectionLink1.get())
                time.sleep(delayTimeBetweenLinks)
                wb.get('browser_1st').open(connectionLink2.get())    
                time.sleep(delayTimeBetweenLinks)
                wb.get('browser_1st').open(connectionLink3.get())    
                time.sleep(delayBetweenWindows)
                windows -=1

        

def Start_Command():
    global Running
    global timeReopen
    global timeClose
    global totalWindows
    global threadRun


    threadRun = threading.Thread(target=Run)
    
    # Get values from input
    timeReopen = 0 # Do once in the beginning then set the time re-open
    totalWindows = float(enTotalWindows.get())
    
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
    connectionLink1 = tk.StringVar()
    connectionLink1.set(defaultConnectionLink1)

    connectionLink2 = tk.StringVar()
    connectionLink2.set(defaultConnectionLink2)

    connectionLink3 = tk.StringVar()
    connectionLink3.set(defaultConnectionLink3)
    # timeReopen = 0 
    # timeClose = 0
    # totalWindows = 0

        #Biến lưu text cho entry
    txtTimeReopen = tk.StringVar()
    txtTimeReopen.set(defaultTimeReopen)
    txtTotalWindows = tk.StringVar()
    txtTotalWindows.set(defaultTotalWindows)

    #biến lưu giá trị cho biết có đang chạy tính năng lặp hay không
    global Running
    Running = False

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # Textbox (Entry) chứa link 
    enConnection1 = tk.Entry(bd=3, width=150, textvariable=connectionLink1)
    enConnection1.pack()

    enConnection2 = tk.Entry(bd=3, width=150, textvariable=connectionLink2)
    enConnection2.pack()

    enConnection3 = tk.Entry(bd=3, width=150, textvariable=connectionLink3)
    enConnection3.pack()

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
    lbl_TimeReopen = tk.Label(root, text ="Reopen the link every: ").place(x=18, y=67)
    lbl_TotalWindows = tk.Label(root, text ="Total tabs: ").place(x=18, y=90)
    lbl_TimeClose_unit = tk.Label(root, text="(seconds)").place(x=222, y=67)
    lbl_TimeReopen_unit = tk.Label(root, text="(seconds)").place(x=222, y=90)
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    root.mainloop()

    
