import tkinter as tk
from Map import Map
from Line_segment import Line_segment
from Point import Point
map = Map()
map.add_object(0, 0, 10)
line_segment1 = Line_segment(Point([-10, 11]), Point([10, 10]))
print(map.intersects_any(line_segment1))

gui=tk.Tk()
width = 500
height = 500
gui.geometry(str(width) + "x" + str(height))
canvas= tk.Canvas(gui,width=width, height=height)
canvas.pack()

map.draw_objects(canvas)

gui.mainloop()