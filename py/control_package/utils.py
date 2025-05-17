"""Utility helpers for reading network data."""

from typing import List, Tuple, Optional, Any

try:
    import networkx as nx  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    nx = None

from .node import Node
from .edge import Edge


def load_network(filename: Optional[str] = None, graph: Optional['nx.Graph'] = None) -> Tuple[int, List[Edge], List[Optional[str]]]:
    """Load a network from a Pajek ``.net`` file or a ``networkx`` graph.

    Parameters
    ----------
    filename : str, optional
        Path to a ``.net`` formatted file.
    graph : :class:`networkx.Graph`, optional
        Graph instance where nodes are 1-indexed integers. If given, ``filename``
        is ignored. Node attribute ``name`` will be used if present.

    Returns
    -------
    tuple
        ``(node_num, edges, names)`` where ``edges`` is a list of :class:`Edge`
        and ``names`` stores optional node labels.
    """

    if graph is not None:
        if nx is None:
            raise ImportError("networkx is required to use the graph parameter")
        node_num = graph.number_of_nodes()
        names: List[Optional[str]] = [None] * (node_num + 1)
        for n, data in graph.nodes(data=True):
            if isinstance(n, int) and 1 <= n <= node_num:
                names[n] = data.get("name")
        edges = [Edge(int(u), int(v)) for u, v in graph.edges()]
        return node_num, edges, names

    if filename is None:
        raise ValueError("either filename or graph must be provided")

    lines = [line.strip() for line in open(filename) if line.strip()]
    if not lines or not lines[0].startswith("*Vertices"):
        raise ValueError("Invalid network file")

    node_num = int(lines[0].split()[1])
    names: List[Optional[str]] = [None] * (node_num + 1)

    idx = 1
    for i in range(1, node_num + 1):
        parts = lines[idx].split()
        if len(parts) > 1:
            names[i] = parts[1]
        idx += 1

    if idx < len(lines) and (lines[idx].startswith("*Edges") or lines[idx].startswith("*Arcs")):
        idx += 1

    edges: List[Edge] = []
    for line in lines[idx:]:
        parts = line.split()
        if len(parts) >= 2:
            src, des = int(parts[0]), int(parts[1])
            edges.append(Edge(src, des))

    return node_num, edges, names
