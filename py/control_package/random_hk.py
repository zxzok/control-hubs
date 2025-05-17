from __future__ import annotations

"""Simplified Hopcroft–Karp maximum matching implementation."""

from typing import List, Set

from .node import Node
from .edge import Edge


class RandomHK:
    """Simplified Hopcroft–Karp maximum matching."""

    def __init__(self, node_src: List[Node], node_des: List[Node], edge: List[Edge | None]):
        """Create a matcher for the bipartite graph defined by ``edge``.

        Parameters
        ----------
        node_src, node_des : list[Node]
            Node containers for the two bipartite sides. Index ``0`` is unused
            so that nodes are 1-indexed.
        edge : list[Edge | None]
            Array of edges where index corresponds to an ``Edge`` object.
        """

        self.nodeSrc = node_src
        self.nodeDes = node_des
        self.edge = edge
        self.nodeNum = len(node_src) - 1
        self.markedSrc = [0] * (self.nodeNum + 1)
        self.markedDes = [0] * (self.nodeNum + 1)
        self.distSrc = [0] * (self.nodeNum + 1)
        self.distDes = [0] * (self.nodeNum + 1)
        self.unMatchedNode: List[int] = []
        self.matchedEdgeList: Set[int] = set()
        self.driverNode: Set[int] = set()
        self.tailNode: Set[int] = set()

    def bfs(self) -> bool:
        """Breadth-first search step of Hopcroft–Karp.

        Returns ``True`` if an augmenting path is found.
        """

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

    def dfs(self, des: int) -> bool:
        """Depth-first search step used to build augmenting paths."""

        for edg in self.nodeDes[des].node_edges:
            src = self.edge[edg].src
            if self.distSrc[src] == self.distDes[des] + 1:
                self.distSrc[src] = 0
                if self.markedSrc[src] == 0 or self.dfs(self.markedSrc[src]):
                    self.markedSrc[src] = des
                    self.markedDes[des] = src
                    return True
        return False

    def find(self):
        """Run the Hopcroft–Karp algorithm."""

        while self.bfs():
            for des in range(1, self.nodeNum + 1):
                if self.markedDes[des] == 0:
                    self.dfs(des)

        for i in range(1, self.nodeNum + 1):
            if self.markedDes[i] == 0:
                self.driverNode.add(i)
            if self.markedSrc[i] == 0:
                self.tailNode.add(i)
            if self.markedDes[i] != 0:
                src = self.markedDes[i]
                for e in self.nodeDes[i].node_edges:
                    if self.edge[e].src == src:
                        self.matchedEdgeList.add(e)
                        break
