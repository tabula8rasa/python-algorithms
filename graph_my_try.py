class Node:

    def __init__(self, name, data=None):
        self.name = name
        self.data = data
        self.neighbors = {}


    def add_neighbor(self, neighbor, weight):

        if neighbor not in self.neighbors:
            self.neighbors[neighbor] = weight