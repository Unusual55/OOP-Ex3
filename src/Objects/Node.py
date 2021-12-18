import random

""" This object represent a vertex in the graph. Every vertex has it's own unique id, which we implemented it as
key and  3 real number coordinates x,y,z which represent it's location in a 3 dimensional space.
Since we could get a Node who don't have any coordinates, we are using a boolean variable which we call pos in
order to know if the node has a position, if it does, then pos will become true, otherwise it will stay false. """


class Node:
    # Regular constructor which accept 4 parameters and set them as this object properties, pos will become true
    # since we get the coordinates values as inputs.
    def __init__(self, id: int, x: float, y: float, z: float) -> None:
        self.key = id
        self.x = x
        self.y = y
        self.z = z
        self.pos = True

    # Non-Position constructor, which accept only one parameter which is the key of the new node, pos will become
    # false since the coordinates does not exist at the moment
    def __init__(self, id: int) -> None:
        self.key = id
        self.pos = False

    # This function return the key of the node
    def getKey(self):
        return self.key

    # This function check if the node has it's x,y,z coordinates using the boolean pos and return true if there
    # are coordinates, otherwise it will return false
    def checkpos(self):
        return self.pos

    # This function check if the node has it's x,y,z coordinates, if it does, the function will return a tuple
    # (x, y, z), otherwise it will return None
    def getpos(self):
        if self.checkpos:
            return (self.x, self.y, self.z)

    # This function get 3 floats numbers as inputs and set them as the new x, y, z coordinates, as well as
    # setting the boolean pos to True
    def setpos(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z
        self.pos = True

    # This function get 6 float numbers as inputs which represent the three ranges of values any x, y and z can
    # be, and set 3 random values of x, y and z from the different ranges as the new position of this node,
    # as well as setting the boolean pos to True
    def setlimitedrandompos(self, minx: float, miny: float, minz: float, maxx: float, maxy: float, maxz: float):
        self.x = random.randrange(minx, maxx)
        self.y = random.randrange(miny, maxy)
        self.z = random.randrange(minz, maxz)
        self.pos = True

    # This function return a string representation of this object by the following format:
    # (i): (x, y, z)
    # Where i is the key of the node, and x, y, z is the components in the coordinate vector
    def __str__(self) -> str:
        return "(", self.key, "): (", self.x, ",", self.y, ",", self.z, ")"

    # This functipn get an object and compare it to this Node, if the object is not a node, then we will return
    # False immediately, otherwise we will check if all of the properties are equal, if they are we will return
    # True, otherwise we will return False
    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Node):
            return False
        if (__o.key == self.key and __o.x == self.x and __o.y == self.y and __o.z == self.z):
            return True
        return False

    def distance(self, o):
        dx = (self.x-o.x)**2
        dy = (self.y-o.y)**2
        dz = (self.z-o.z)**2
        from math import sqrt
        return sqrt(dx+dy+dz)

