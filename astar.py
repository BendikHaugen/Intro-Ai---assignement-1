"""
from MAP:
INIT(mab_obj(task=x)) : x sets the map
read map is used by init, as well as fill_critical_positions

Get_cell_value : returns value at a position
get_goal_pos : returns goal position
get_end_goal_pos : returns the final goal, if it moves
get_maps : ruturns two numpy arrays, as ints_map and str_map (integer/string matrixes)
twodimentianal lists using numpy is not indexed as [x][y], but
rather indexed as [x, y]
move_goal_pos : used in tick
set_cell_value : sets a value in the map
print map : prints map
pick_move -> used in moving the goal
Replace_map_values replaces two coordinates, and makes sure you dont overwrite G
Tick -> movable goal, call tick after every move, will change the goal pos
show map: shows map - uses string if not provided by another map
"""
class Node():
    def __init__(self, pos, parent=None):
        # Initial values
        self.parent, self.pos = parent, pos
        self.children = []
        self.f, self.g, self.h = 0, 0 ,0

    def addChild(self, child):
        self.children.append(child)

    def checkPosition(self, node):
        return self.pos == node.pos


def aStar(map):
    """this implementation of the aStar Algorithm is based entirely on the appendix "Essentials of the A* algorithm"
    provided in the course TDT4136 at NTNU"""
    OPEN = []
    CLOSED = []
    start_node = Node(map.get_start_pos(), None)
    goal = map.get_goal_pos()
    OPEN.append(start_node) #adds first node
    currentNode = start_node

    while currentNode.pos != goal:
        if len(OPEN) == 0:
            #if goal not found, tell and break
            print("no path found")
            break
        OPEN.sort(key = lambda node: node.f) #sorts the OPEN list, with smallest f value first
        currentNode = OPEN.pop(0)
        CLOSED.append(currentNode)
        if currentNode.pos == goal:
            #returns the goal when its found
            return currentNode 
        else:
            succ = []
            for adj_nodes in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                #Checks neighbouring tiles, and adds as succsessors
                successor_pos = [currentNode.pos[0] + adj_nodes[0], currentNode.pos[1] + adj_nodes[1]]
                if map.get_cell_value(successor_pos) != -1:
                    #only adds node ass successor it its not a wall
                    succ.append(Node(successor_pos, currentNode))

            for successor in succ:
                # checks if the succsessor already is in OPEN
                if any(successor.checkPosition(node) for node in OPEN):
                    successor = next(node for node in OPEN if successor.checkPosition(node))
                currentNode.addChild(successor)
                if (successor not in OPEN) and (successor not in CLOSED):
                    #evaluates and adds to open if not in either CLOSED or OPEN
                    attach_and_eval(successor, currentNode, goal,map)
                    OPEN.append(successor)
                elif currentNode.g + map.get_cell_value(successor.pos) < successor.g:
                    # updates parent if there is a better path
                    attach_and_eval(successor, currentNode, goal,map)
                    propagate_path_improvements(currentNode,map)


# Gives child parent and finds it values               
def attach_and_eval(child, parent, goal, map):
    child.parent = parent
    child.g = child.parent.g + map.get_cell_value(child.pos)
    child.h = abs(goal[0] - child.pos[0])+ abs(goal[1] - child.pos[1])
    child.f = child.g + child.h


def propagate_path_improvements(parent, map):
    for child in parent.children:
        if parent.g + map.get_cell_value(child.pos) < child.g:
            child.parent = parent
            child.g = parent.g + map.get_cell_value(child.pos)
            child.f = child.g + child.h
            propagate_path_improvements(child, map)


def trace_path(node):
    #creates the path from start to goal
    path = []
    thisNode = node
    while thisNode is not None:
        path.append(thisNode.pos)
        thisNode = thisNode.parent
    return path

def finalpath(map, path):
        stringMap = map.str_map
        for pos in path:
            #sets path = '' to create visual
            stringMap[pos[0]][pos[1]] = ''
        map.show_map(stringMap)
