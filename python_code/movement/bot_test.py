from ..movement.Robot import Robot
from ..map.Map import Map
import numpy as np
bot = Robot()
map = Map()
map.add_object(0.5, 0, 0.1)
p1 = map.add_point_from_position([0, 0])
p3 = map.add_point_from_position([0.5, 0.5])
p2 = map.add_point_from_position([1, 0])

# map.add_points_in_grid()
map.add_all_possible_line_segments()
path = map.find_path(p1, p2)
print(path)

bot.move_along_path(path)