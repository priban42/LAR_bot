from map import Map
from map import Vizualize

gui = Vizualize()
map = Map()
map.add_object(0.5, 0, 0.1)
#p1 = map.add_point_from_position([0, 0])
#p3 = map.add_point_from_position([0.5, 0.5])
#p2 = map.add_point_from_position([1, 0])

map.add_points_in_grid()
map.add_all_possible_line_segments()
#path = map.find_path(p1, p2)
#print(path)
#for n in path:
#    print (n.position)
print("points:", len(map.points))
print("line_segments:", len(map.line_segments))
gui.set_map(map)
gui.draw()