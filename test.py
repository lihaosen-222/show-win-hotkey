import keyboard
import win32gui
import pythoncom
from win32.lib import win32con
from win32com import client

win = {}


def ctrl_shift(i):
    win[i] = win32gui.GetForegroundWindow()
    print('绑定', win32gui.GetWindowText(win[i]))

def ctrl(i):
    if(not win.get(i)): 
        return

    if win32gui.IsIconic(win[i]):
        win32gui.ShowWindow(win[i], win32con.SW_SHOWNORMAL) # 最小化的时候显示到最前
    else:
        # 这四行不加 SetForegroundWindow 会报错，原理我也不知道
        win32gui.BringWindowToTop(win[i])
        pythoncom.CoInitialize()
        shell = client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(int(win[i])) # 没最小化的时候显示到最前
    print('显示', win32gui.GetWindowText(win[i])) 


for i in range(1, 6):
    keyboard.add_hotkey('alt+'+str(i), ctrl, (i,))
    keyboard.add_hotkey('alt+shift+'+str(i), ctrl_shift, (i,))

keyboard.wait('alt+shift+q')
input('Press Enter to exit…')
