from Tkinter import *
from PIL import Image, ImageTk

master = Tk()

img = Image.open("Bloomberg1.png")
w, h = img.size

canvas = Canvas(master, width=w, height=h)
canvas.pack()

photo = ImageTk.PhotoImage(img)
canvas.create_image(0,0, anchor=NW, image=photo)

mainloop()
