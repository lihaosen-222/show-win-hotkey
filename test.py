import keyboard
import win32gui
import pythoncom
from win32.lib import win32con
from win32com import client
import time

win = {}


def getThrottleFn(fn, break_time):
    ref = {'pre_time': 0}
    # print(ref)
    
    def throttleFn(*a):
        
        now = time.time()
        
        if now - ref['pre_time'] > break_time:
            fn(*a)
        # print(now - ref['pre_time'] > break_time)
        ref['pre_time'] = now
        
    return throttleFn

def ctrl_shift(i):
    win[i] = win32gui.GetForegroundWindow()
    print('绑定', win32gui.GetWindowText(win[i]))

def ctrl(i):
    print('start', i)
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


alt_throttle = getThrottleFn(ctrl,0.1)

for i in range(1, 6):
    keyboard.add_hotkey('alt+'+str(i), alt_throttle, (i,))
    keyboard.add_hotkey('alt+shift+'+str(i), ctrl_shift, (i,))

keyboard.wait('alt+shift+q')
input('Press Enter to exit…')
