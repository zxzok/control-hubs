from __future__ import annotations

"""Computation of maximum matching based control schemes."""

from typing import List, Set, Optional

try:
    import networkx as nx  # type: ignore
except Exception:  # pragma: no cover
    nx = None

from .node import Node
from .edge import Edge
from .utils import load_network
from .random_hk import RandomHK


class ControlSchemes:
    """Compute maximum matching and driver nodes for a network."""

    def __init__(self, input_file: Optional[str] = None, *, graph: Optional['nx.Graph'] = None, output_file: str = "./result/find_schemes.txt"):
        """Run maximum matching on the given network.

        Parameters
        ----------
        input_file : str, optional
            Path to a ``.net`` file describing the network.
        graph : :class:`networkx.Graph`, optional
            Graph object to use instead of ``input_file``.
        output_file : str, optional
            File where the resulting scheme is written.
        """

        if graph is not None and nx is None:
            raise ImportError("networkx is required to use the graph parameter")
        node_num, edges_list, names = load_network(input_file, graph)
        self.nodeNum = node_num
        self.edgeNum = len(edges_list)
        self.nodeSrc: List[Node] = [Node(i) for i in range(node_num + 1)]
        self.nodeDes: List[Node] = [Node(i) for i in range(node_num + 1)]
        self.edge: List[Edge | None] = [None] * (self.edgeNum + 1)
        for idx, e in enumerate(edges_list, start=1):
            self.edge[idx] = e
            self.nodeSrc[e.src].node_edges.append(idx)
            self.nodeDes[e.des].node_edges.append(idx)

        self.output_file = output_file
        self.find()

    def find(self):
        """Execute the Hopcroft–Karp routine and write results."""
        hk = RandomHK(self.nodeSrc, self.nodeDes, self.edge)
        hk.find()

        with open(self.output_file, "w") as f:
            f.write("maximum matching edgeID for scheme1:\n")
            f.write(" ".join(str(e) for e in sorted(hk.matchedEdgeList)) + "\n")
            f.write("minimum driver node set for scheme1:\n")
            f.write(" ".join(str(n) for n in sorted(hk.driverNode)) + "\n")
