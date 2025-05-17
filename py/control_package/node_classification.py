from __future__ import annotations

"""Classify nodes into head, tail and control hub categories."""

from typing import List, Set, Optional

try:
    import networkx as nx  # type: ignore
except Exception:  # pragma: no cover
    nx = None

from .node import Node
from .edge import Edge
from .utils import load_network


class NodeClassification:
    """Identify head, tail and control hub nodes in a directed network."""

    def __init__(self, input_file: Optional[str] = None, *, graph: Optional['nx.Graph'] = None, output_file: str = "./result/nodeType.txt"):
        """Compute the node types.

        Parameters
        ----------
        input_file : str, optional
            Path to a ``.net`` file defining the network.
        graph : :class:`networkx.Graph`, optional
            Graph object describing the network. Overrides ``input_file`` if
            provided.
        output_file : str, optional
            Location where a text report will be written.
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

        self.markedSrc = [0] * (node_num + 1)
        self.markedDes = [0] * (node_num + 1)
        self.distSrc = [0] * (node_num + 1)
        self.distDes = [0] * (node_num + 1)
        self.unMatchedNode: List[int] = []

        self.Control_hub: Set[int] = set()
        self.Head: Set[int] = set()
        self.Tail: Set[int] = set()

        self.judge(output_file)

    def initialize(self):
        """Reset matching markers and distance arrays."""
        for i in range(1, self.nodeNum + 1):
            self.markedSrc[i] = 0
            self.markedDes[i] = 0
            self.distSrc[i] = 0
            self.distDes[i] = 0
        self.unMatchedNode = []

    def judge(self, output_file: str):
        """Compute node categories and write them to ``output_file``."""

        # Step1, find tail nodes
        self.initialize()
        while self.BFS_APU():
            for src in range(1, self.nodeNum + 1):
                if self.markedSrc[src] == 0:
                    self.DFS_APU(src)
        self.Tail.update(self.unMatchedNode)

        # Step2, find head nodes
        self.initialize()
        while self.BFS_APD():
            for des in range(1, self.nodeNum + 1):
                if self.markedDes[des] == 0:
                    self.DFS_APD(des)
        self.Head.update(self.unMatchedNode)

        # Step3, control hubs
        for i in range(1, self.nodeNum + 1):
            if i not in self.Head and i not in self.Tail:
                self.Control_hub.add(i)

        with open(output_file, "w") as f:
            for i in range(1, self.nodeNum + 1):
                if i in self.Head and i not in self.Tail:
                    f.write(f"{i}: head\n")
                elif i in self.Tail and i not in self.Head:
                    f.write(f"{i}: Tail\n")
                elif i in self.Head:
                    f.write(f"{i}: Head,Tail\n")
                elif i in self.Control_hub:
                    f.write(f"{i}: Control_hub\n")

    def BFS_APU(self) -> bool:
        """BFS on the source side used by Hopcroft–Karp."""

        flag = False
        self.unMatchedNode = []
        for i in range(1, self.nodeNum + 1):
            self.distDes[i] = 0
            self.distSrc[i] = 0
            if self.markedSrc[i] == 0:
                self.unMatchedNode.append(i)
        idx = 0
        while idx < len(self.unMatchedNode):
            src = self.unMatchedNode[idx]
            idx += 1
            for edg in self.nodeSrc[src].node_edges:
                des = self.edge[edg].des
                if self.distDes[des] == 0:
                    self.distDes[des] = self.distSrc[src] + 1
                    if self.markedDes[des] == 0:
                        flag = True
                    else:
                        if self.distSrc[self.markedDes[des]] == 0:
                            self.distSrc[self.markedDes[des]] = self.distDes[des] + 1
                            self.unMatchedNode.append(self.markedDes[des])
        return flag

    def DFS_APU(self, src: int) -> bool:
        """DFS helper for augmenting paths from source side."""

        for edg in self.nodeSrc[src].node_edges:
            des = self.edge[edg].des
            if self.distDes[des] == self.distSrc[src] + 1:
                self.distDes[des] = 0
                if self.markedDes[des] == 0 or self.DFS_APU(self.markedDes[des]):
                    self.markedDes[des] = src
                    self.markedSrc[src] = des
                    return True
        return False

    def BFS_APD(self) -> bool:
        """BFS on the destination side used by Hopcroft–Karp."""

        flag = False
        self.unMatchedNode = []
        for i in range(1, self.nodeNum + 1):
            self.distSrc[i] = 0
            self.distDes[i] = 0
            if self.markedDes[i] == 0:
                self.unMatchedNode.append(i)
        idx = 0
        while idx < len(self.unMatchedNode):
            des = self.unMatchedNode[idx]
            idx += 1
            for edg in self.nodeDes[des].node_edges:
                src = self.edge[edg].src
                if self.distSrc[src] == 0:
                    self.distSrc[src] = self.distDes[des] + 1
                    if self.markedSrc[src] == 0:
                        flag = True
                    else:
                        if self.distDes[self.markedSrc[src]] == 0:
                            self.distDes[self.markedSrc[src]] = self.distSrc[src] + 1
                            self.unMatchedNode.append(self.markedSrc[src])
        return flag

    def DFS_APD(self, des: int) -> bool:
        """DFS helper for augmenting paths from destination side."""

        for edg in self.nodeDes[des].node_edges:
            src = self.edge[edg].src
            if self.distSrc[src] == self.distDes[des] + 1:
                self.distSrc[src] = 0
                if self.markedSrc[src] == 0 or self.DFS_APD(self.markedSrc[src]):
                    self.markedSrc[src] = des
                    self.markedDes[des] = src
                    return True
        return False
