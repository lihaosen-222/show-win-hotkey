import keyboard
import win32gui
from win32.lib import win32con


# Snake Case 下划线命名法
# pip freeze > requirements.txt
# pip install -r requirements.txt


win = {}


def ctrl_shift(i):
    win[i] = win32gui.GetForegroundWindow()

def ctrl(i):
    if(not win.get(i)): 
        return
    if win32gui.IsIconic(win[i]):
        win32gui.ShowWindow(win[i], win32con.SW_SHOWNORMAL)
        
    else:
        win32gui.ShowWindow(win[i], win32con.SW_SHOWMINIMIZED)


for i in range(1, 6):
    keyboard.add_hotkey('ctrl+'+str(i), ctrl, (i,))
    keyboard.add_hotkey('ctrl+shift+'+str(i), ctrl_shift, (i,))
# keyboard.add_hotkey('ctrl+q', ctrl_q)
# keyboard.add_hotkey('ctrl+1', ctrl_1)
# keyboard.add_hotkey('ctrl+2', ctrl_2)
keyboard.wait('ctrl+shift+q')
input('Press Enter to exit…')
