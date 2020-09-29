from room import Room
from player import Player
from world import World


import random
from ast import literal_eval

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)
    
    
# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

#helper function for opposite directions in case we need to go back the way we came

def opp_dir(dir):
    if dir == "n":
        return "s"
    elif dir == "s":
        return "n"
    elif dir == "e":
        return "w"
    elif dir == "w":
        return "e"

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room

#moves added to a stack
moves = Stack()

#visited rooms = total rooms
while len(visited_rooms) < len(world.rooms):
    exits = player.current_room.get_exits()
    available_directions = []
    for exit in exits:
        #if room towards exit has not been visited, add it to direction
        if (exit is not None) and (player.current_room.get_room_in_direction(exit) not in visited_rooms):
            available_directions.append(exit)
            
    #set current rooms to visited
    visited_rooms.add(player.current_room)
    
    #if there any availble directions
    if len(available_directions) > 0:
        #random
        random_direction_index = random.randint(0, len(available_directions) - 1)
        #add to stack
        moves.push(available_directions[random_direction_index])
        #add to traversal path
        traversal_path.append(available_directions[random_direction_index])
        
    #if there are no directions remaining
    else:
        last_move = moves.pop()
        #player turns back
        player.travel(opp_dir(last_move))
        #add to travel path
        traversal_path.append(opp_dir(last_move))


for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
