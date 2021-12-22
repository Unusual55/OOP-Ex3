from Objects.Node import Node


class Vector:
    def __init__(self, x: tuple, y: tuple, z: tuple, src: Node, dest: Node):
        self._x = dest.get_x() - src.get_x()
        self._y = dest.get_y() - src.get_y()
        if z[0] == 0.0 and z[1] == 0:
            x_to_z = (x[1] - self._x) / (x[1] - x[0])
            y_to_z = (y[1] - self._y) / (y[1] - y[0])
            self._z = (x_to_z + y_to_z) / 2
        else:
            self._z = dest.get_z() - src.get_z()

    def get_vector(self):
        return self._x, self._y, self._z
