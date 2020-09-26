from Map import Map_Obj
from astar import *


# Iterates through task 1,2,3 and 4 and displays all shortest paths
for i in [1,2,3,4]:
    map = Map_Obj(task=i)
    end_node= aStar(map)
    path = trace_path(end_node)
    finalpath(map, path)
