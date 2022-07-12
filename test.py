import keyboard
import win32gui
import pythoncom
from win32.lib import win32con
from win32com import client
import time
import httpx
import asyncio

# 注册异步请求
async def myrequest():
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            'http://localhost:3000/api/getTodayStatus'
        )
        result = resp.text
        print(result)
loop = asyncio.get_event_loop()

win = {}

def getThrottleFn(fn, break_time):
    ref = {'pre_time': 0}
    def throttleFn(*a):
        now = time.time()
        if now - ref['pre_time'] > break_time:
            fn(*a)
        ref['pre_time'] = now
        
    return throttleFn

def alt_shift(i):
    win[i] = win32gui.GetForegroundWindow()
    print('绑定', win32gui.GetWindowText(win[i]))

def alt(i):
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

    # 异步执行请求
    loop.run_until_complete(myrequest())


alt_throttle = getThrottleFn(alt,0.1)

for i in range(1, 6):
    keyboard.add_hotkey('alt+'+str(i), alt_throttle, (i,))
    keyboard.add_hotkey('alt+shift+'+str(i), alt_shift, (i,))

keyboard.wait('alt+shift+q')

input('Press Enter to exit…')


