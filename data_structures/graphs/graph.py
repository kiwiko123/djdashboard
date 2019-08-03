import abc
from data_structures.graphs.properties import Edge, Vertex


class _BaseGraph(metaclass=abc.ABCMeta):

    def __init__(self):
        self._adjacency_map = {}

    def vertex_count(self) -> int:
        pass

    def edge_count(self) -> int:
        pass

    def is_complete(self) -> bool:
        """
        Returns True if this is an undirected graph with an edge
        between every pair of vertices.
        """
        pass

    def is_subgraph(self, other_graph) -> bool:

        pass

    def is_spanning_subgraph(self, other_graph) -> bool:
        """
        Returns True if other_graph is a subgraph that contains
        all vertices of this graph.
        """
        pass

    def is_connected(self) -> bool:
        """
        Returns True if this is an undirected graph with a path
        between any pair of vertices.
        """
        pass

    def has_cycle(self) -> bool:
        """
        Returns True if this graph contains a cycle.
        """
        pass

    def is_tree(self) -> bool:
        """
        Returns True if this is a connected, acyclic graph.
        """
        pass


class UndirectedGraph(_BaseGraph):

    def __init__(self):
        super().__init__()