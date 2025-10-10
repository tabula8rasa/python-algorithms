class Node:

    def __init__(self, name, data=None):
        self.name = name
        self.data = data
        self.neighbors = {}


    def add_neighbor(self, neighbor, weight):

        if neighbor not in self.neighbors:
            self.neighbors[neighbor] = weight

    def remove_neighbor(self, neighbor):

        if neighbor in self.neighbors:
            del self.neighbors[neighbor]

    def get_neighbors(self):

        return list(self.neighbors.keys())

    def get_weight_to_neighbor(self, neighbor):
