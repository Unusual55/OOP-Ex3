""" This class represent a set of integers which represent the set of keys which have an edge
from them to the key of this set. This object contains a key, which represent the id of it's node and
a set of integers which contain the keys of the node who have an edge from them to the key node.
We are using custom set in order to reduce the time complexity of searching, adding or removing nodes
and edges from the graph, as well as the space complexity, since we are keep only the keys of the nodes
 instead of saving the whole Node or the Whole edge. Another advantage to this concept is to prevent any
 chance that we might have duplicate edges since we keep the Edges only in one place, and using only
 the keys we need in order to access and modify the map of the graph as needed"""


class ReversedEdgesSet:
    # This constructor get no input and create an empty set
    def __init__(self, ):
        self.set = set()

    # This function get one integer input which is the key of the source node we want to add, and add
    # it to the set
    def add_edge(self, src: int):
        self.set.add(src)

    # This function get one integer input which is the key of the source node we want to remove from
    # the set, and if it exists, the function will remove it, otherwise it will raise an exception
    def remove_edge(self, src: int):
        if not (src in self.set):
            raise Exception("The source id doesn't exist in the set")
        self.set.remove(src)

    # This function get one integer input which is the key of the source node we want to check if the
    # set contains it, and return True if it does, otherwise it will return False
    def contains_edge(self, src: int):
        return src in self.set

    # This function return a copy of the set in order to return the keys of the nodes we keep inside it
    def get_keys(self):
        return self.set.copy()

    # This function remove every element in the set
    def clear_set(self):
        return self.set.clear()
