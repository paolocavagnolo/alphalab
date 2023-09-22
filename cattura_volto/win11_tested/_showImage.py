from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
import sys
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("echo")     # naming it "echo"
args = parser.parse_args()  # returns data from the options specified (echo)

image_path = args.echo

def close_window ():
    global root
    root.destroy()

pilImage = Image.open(image_path)

height = pilImage.size[1]
width = pilImage.size[0]

new_height = 1024
new_width  = int(new_height * width / height)

pilImage = pilImage.rotate(90)

pilImage = pilImage.resize((new_width, new_height), Image.LANCZOS)

root = Tk()

w, h = root.winfo_screenwidth(), root.winfo_screenheight()

root.attributes('-fullscreen', True)
root.geometry("%dx%d+0+0" % (w, h))
root.focus_set()
root.bind("<Escape>", lambda e: root.destroy())
root.after(5000,lambda:root.withdraw())
root.after(5100,lambda:root.destroy())

canvas = Canvas(root,width=w,height=h,highlightthickness=0)
canvas.pack()
canvas.configure(background='black')

imgWidth, imgHeight = pilImage.size

if imgWidth > w or imgHeight > h:
    ratio = min(w/imgWidth, h/imgHeight)
    imgWidth = int(imgWidth*ratio)
    imgHeight = int(imgHeight*ratio)
    pilImage = pilImage.resize((imgWidth,imgHeight), Image.ANTIALIAS)

image = ImageTk.PhotoImage(pilImage)
imagesprite = canvas.create_image(w/2,h/2,image=image)

root.mainloop()


