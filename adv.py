from room import Room
from player import Player
from world import World
from util import Graph, Stack, Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

graph = Graph()
stack = Stack()
stack.push(world.starting_room)

visited = set()

while stack.size() > 0:
    room = stack.pop()
    room_id = room.id

    if room_id not in graph.vertices:
        graph.add_vertex(room_id)

    exits = room.get_exits()

    for direction in exits:
        exit_room = room.get_room_in_direction(direction)
        exit_room_id = exit_room.id

        if exit_room_id not in graph.vertices:
            graph.add_vertex(exit_room_id)

        graph.add_edge(room_id, exit_room_id, direction)

        if exit_room_id not in visited:
            stack.push(exit_room)

    visited.add(room_id)


def bfs(room_id, visited, graph_=graph):
    """
    Search for the nearest unvisited space using a BFS approach

    Args:
        room_id (int)
        visited (set)
        graph   (graph)

    Returns:
        list of moves that the player can take to get to the nearest unvisited space
    """
    queue = Queue()
    queue.enqueue([room_id, []])

    visited_bfs = set()
    visited_bfs.add(room_id)

    while queue.size() > 0:
        room, moves = queue.dequeue()

        neighbors = graph_.get_neighbors(room)

        neighbors_keys = list(neighbors.keys())

        if len(neighbors_keys) == 1 and neighbors[neighbors_keys[0]] not in visited:
            # Return set of directions for player to traverse
            dead_end = list(moves) + [neighbors_keys[0]]
            return dead_end
        else:
            for direction in neighbors:
                next_room = neighbors[direction]
                new_moves = moves + [direction]

                if next_room not in visited_bfs:
                    queue.enqueue([next_room, new_moves])
                    visited_bfs.add(next_room)
                if next_room not in visited:
                    return new_moves


# Fill this out with directions to walk
traversal_path = []
visited = set()
visited.add(world.starting_room.id)
current_room_id = world.starting_room.id
num_rooms = len(graph.vertices)

while len(visited) < num_rooms:
    moves = bfs(current_room_id, visited)

    for direction in moves:
        player.travel(direction)
        traversal_path.append(direction)
        visited.add(player.current_room.id)
    current_room_id = player.current_room.id


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
