import tkinter as tk
from Map import Map
from Line_segment import Line_segment
from Point import Point
map = Map()
map.add_object(0, 0, 100)
map.add_line_segment_from_positions([-100, -100], [300, 150])

gui=tk.Tk()
width = 900
height = 500
gui.geometry(str(width) + "x" + str(height))
canvas= tk.Canvas(gui,width=width, height=height)
canvas.pack()

map.draw(canvas)

gui.mainloop()