from __future__ import annotations

"""Utilities to detect sensitive control hubs."""

from typing import List, Set, Optional

try:
    import networkx as nx  # type: ignore
except Exception:  # pragma: no cover
    nx = None

from .utils import load_network
from .node_classification import NodeClassification


class FindSensitiveControlHub:
    """Identify control hubs sensitive to edge removal."""

    def __init__(self, input_file: Optional[str] = None, *, graph: Optional['nx.Graph'] = None, output_file: str = "./result/sensitive_control_hub.txt"):
        if graph is not None and nx is None:
            raise ImportError("networkx is required to use the graph parameter")
        node_type = NodeClassification(input_file, graph=graph)
        self.init_control_hub = node_type.Control_hub
        node_num, edges_list, names = load_network(input_file, graph)
        self.nodeNum = node_num
        self.edgeNum = len(edges_list)
        self.names = names
        self.edges_list = edges_list
        self.output_file = output_file
        self.temp_file = "./net/temp.net"
        self.sensitive_control_hub: Set[int] = set()
        self.find()

    def _write_network_without_edge(self, edge_idx: int):
        """Write a temporary network file with one edge removed."""
        with open(self.temp_file, "w") as f:
            f.write(f"*Vertices {self.nodeNum}\n")
            for i in range(1, self.nodeNum + 1):
                name = self.names[i] if i < len(self.names) else ""
                if name is None:
                    f.write(f"{i}\n")
                else:
                    f.write(f"{i}\t{name}\n")
            f.write("*Edges\n")
            for j, e in enumerate(self.edges_list, start=1):
                if j != edge_idx:
                    f.write(f"{e.src}\t{e.des}\n")

    def find(self):
        """Compute sensitive control hubs by edge removal."""
        for idx in range(1, self.edgeNum + 1):
            self._write_network_without_edge(idx)
            temp_ch = NodeClassification(self.temp_file)
            for hub in self.init_control_hub:
                if hub not in temp_ch.Control_hub:
                    self.sensitive_control_hub.add(hub)

        with open(self.output_file, "w") as f:
            f.write("sensitive control hub id:\n")
            for h in sorted(self.sensitive_control_hub):
                f.write(f"{h}\n")
