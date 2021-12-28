""" This class represent an edge in the graph. every edge is a unique pair of node's ids which
    represent the source vertex and the destination vertex. let e=(u,v) be an edge, then u is the
     source of the edge and v is the destination of the edge.
     Since the Graph is Directed Weighted Graph, then every edge is unique: (u,v) is different from
     (v,u), and every edge have a weight"""


class Edge:
    def __init__(self, src: int, dest: int, w: float):
        self.src = src
        self.dest = dest
        self.w = w

    # This function returns the id of the source vertex of this Edge
    def get_src(self):
        return self.src

    # This function returns the id of the destination vertex of this Edge
    def get_dest(self):
        return self.dest

    # This function returns the weight of this edge
    def get_weight(self):
        return self.w

    # This function set a new weight for this edge
    def set_weight(self, weight: float):
        if weight <= 0:
            raise Exception("The weight cannot be 0 or negative")
        self.w = weight

    # This function returns a string representation of this edge according to the following format:
    # (u-> v): w
    # Legend: u is the id of the source vertex, v is the id of the destination vertex and w is the weight
    def __str__(self):
        return f"({str(self.src)}-> {str(self.dest)}): {str(self.w)}"

    # This function get an object and check if it equals to this edge, if it's not an edge object, then
    # we will return false immediately, if it is an edge, if all the properties are equal between
    # other and this edge, then the function will return True, otherwise it will return False
    def __eq__(self, other):
        if not isinstance(other, Edge):
            return False
        return (other.src == self.src) and (other.dest == self.dest) and (other.w == self.w)
    
    # This function allow us to hash the Edge object
    def __hash__(self):
        return hash(str(self))

    # This function return a dictionary which contains the information of the edge in order to save it to .json
    def edge_to_dict(self):
        return {
            "src": self.src,
            "w": self.w,
            "dest": self.dest
        }
