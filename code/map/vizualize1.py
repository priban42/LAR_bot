import random
import tkinter as tk
from Map import Map
from Line_segment import Line_segment
from Point import Point
map = Map()
map.add_object(0, 0, 50)
map.add_object(0, 100, 50)
po = []
for a in range(10):
    pos = [random.randint(-200, 200), random.randint(-200, 200)]
    po.append(map.add_point_from_position(pos))
for a in range(len(po)):
    for b in range(a+1, len(po)):
        map.add_line_segmetn_from_points(po[a], po[b])
path = map.find_path(po[0], po[1]).nodes
for p in path:
    print(p.position)

print(map.graph)
gui=tk.Tk()
width = 900
height = 500
gui.geometry(str(width) + "x" + str(height))
canvas= tk.Canvas(gui,width=width, height=height)
canvas.pack()

map.draw(canvas)

gui.mainloop()