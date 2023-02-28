import tkinter as tk
from Map import Map

map = Map()
map.add_object(110, 110)

gui=tk.Tk()
width = 500
height = 500
gui.geometry(str(width) + "x" + str(height))
canvas= tk.Canvas(gui,width=width, height=height)
canvas.pack()

map.draw_objects(canvas)
print('bagr bagr')
gui.mainloop()