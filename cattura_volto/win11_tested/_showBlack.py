from tkinter import *
from tkinter.ttk import *
import sys


def close_window ():
    global root
    root.destroy()

root = Tk()

w, h = root.winfo_screenwidth(), root.winfo_screenheight()

root.attributes('-fullscreen', True)
root.geometry("%dx%d+0+0" % (w, h))
root.focus_set()
root.bind("<Escape>", lambda e: root.destroy())

canvas = Canvas(root,width=w,height=h,highlightthickness=0)
canvas.pack()
canvas.configure(background='black')

root.mainloop()


