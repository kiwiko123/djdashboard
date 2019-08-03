

class Vertex:
    def __init__(self, value):
        self._value = value
        self._in_edge = None
        self._out_edge = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value) -> None:
        self._value = new_value

    @property
    def incoming_edge(self):
        return self._in_edge

    @incoming_edge.setter
    def incoming_edge(self, new_in_edge) -> None:
        _verify_type(new_in_edge, Edge)
        self._in_edge = new_in_edge

    @property
    def outgoing_edge(self):
        return self._out_edge

    @outgoing_edge.setter
    def outgoing_edge(self, new_out_edge) -> None:
        _verify_type(new_out_edge, Edge)
        self._out_edge = new_out_edge

    @property
    def degree(self) -> int:
        """
        The number of edges incident on this vertex.
        """
        return 2

    def is_incident_on(self, edge: 'Edge') -> bool:
        """
        Returns True if the edge is connected to this vertex.
        """
        return edge in (self.incoming_edge, self.outgoing_edge)



class Edge:
    def __init__(self, origin: Vertex, destination: Vertex, weight=None):
        self._origin = origin
        self._destination = destination
        self._weight = weight

    @property
    def origin(self) -> Vertex:
        return self._origin

    @origin.setter
    def origin(self, new_origin: Vertex) -> None:
        _verify_type(new_origin, Vertex)
        self._origin = new_origin

    @property
    def destination(self) -> Vertex:
        return self._destination

    @destination.setter
    def destination(self, new_destination: Vertex) -> None:
        _verify_type(new_destination, Vertex)
        self._destination = new_destination

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, new_weight) -> None:
        self._weight = new_weight

    def is_incident_on(self, vertex: Vertex) -> bool:
        """
        Returns True if the vertex is connected to this edge.
        """
        return vertex in (self.origin, self.destination)


def _verify_type(obj, expected_type: type) -> None:
    obj_type = type(obj)
    if not (isinstance(obj, expected_type) or issubclass(obj_type, expected_type)):
        raise TypeError('{0} is not of type {1}'.format(obj, expected_type))


if __name__ == '__main__':
    pass