class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, v_id):
        self.vertices[v_id] = {}

    def add_edge(self, v1, v2, direction):
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1][direction] = v2
        else:
            raise KeyError("One or both vertex not in graph")

    def get_neighbors(self, v_id):
        if v_id in self.vertices:
            return self.vertices[v_id]
        else:
            raise KeyError("Vertex not valid")


class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


class Stack:
    def __init__(self):
        self.stack = []

    def push(self, val):
        self.stack.append(val)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)
