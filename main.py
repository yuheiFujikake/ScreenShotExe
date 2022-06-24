import ctypes
from ctypes import wintypes
import keyboard
from tkinter import *
import tkinter as tk
from tkinter import filedialog
import os
import pyautogui
import datetime


class ScreenShotTool:
    APP_TITL = "ScreenShotTool"

    def __init__(self):
        self.frame = 1
        self.root = tk.Tk()
        self.uri = StringVar()
        self.uri.set(os.path.expanduser('~'))

    def createFileName(self) -> str:
        now = datetime.datetime.now()
        return now.strftime('%Y%m%d%_H%M%S.png')

    def doScreenShot(self):
        window = pyautogui.getActiveWindow()
        config = ctypes.windll.dwmapi.DwmGetWindowAttribute
        rect = wintypes.RECT()
        DWMWA_EXTENDED_FRAME_BOUNDS = 9
        config(ctypes.wintypes.HWND(window._hWnd),
               ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
               ctypes.byref(rect),
               ctypes.sizeof(rect)
               )

        width = rect.right - rect.left
        height = rect.bottom - rect.top
        img = pyautogui.screenshot(region=(rect.left, rect.top, width, height))
        img.save(self.uri.get()+"/" + self.createFileName())

    def redisplay(self):
        self.root.deiconify()
        keyboard.remove_hotkey('alt+p')
        keyboard.remove_hotkey('alt+l')
        keyboard.remove_hotkey('esc')

    def stopWatchKey(self):
        self.stop()

    def watchKeyPress(self):
        keyboard.add_hotkey('alt+p', self.doScreenShot)
        keyboard.add_hotkey('alt+l', self.redisplay)
        keyboard.add_hotkey('esc', self.stopWatchKey)

    def start(self):
        self.root.withdraw()
        self.watchKeyPress()

    def stop(self):
        self.root.destroy()

    def askDirectory(self):
        path = filedialog.askdirectory(initialdir=self.uri)
        self.uri.set(path)

    def addHeaderFrame(self):
        frame = tk.Frame(self.root, pady=5)
        frame.grid(row=0, column=1, sticky=W)
        label = tk.Label(frame, text='保存先')
        label.pack(side=LEFT, padx=5)
        entry = tk.Entry(frame, textvariable=self.uri, width=50)
        entry.pack(side=LEFT, padx=5)
        btn = tk.Button(frame, text="参照", command=self.askDirectory)
        btn.pack(side=LEFT, padx=5)

    def addFooterFrame(self):
        frame = tk.Frame(self.root, pady=5)
        frame.grid(row=1, column=1, sticky=E)
        submit = tk.Button(frame, text="開始", command=self.start, padx=10)
        submit.pack(side=LEFT, padx=5)
        cabcel = tk.Button(frame, text="キャンセル", command=self.stop, padx=10)
        cabcel.pack(side=LEFT, padx=5)

    def creatGUI(self):
        self.root.title = self.APP_TITL
        self.addHeaderFrame()
        self.addFooterFrame()

    def run(self):
        self.creatGUI()
        self.root.mainloop()


sse = ScreenShotTool()
sse.run()
