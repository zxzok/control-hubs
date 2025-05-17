"""Graph node representation used by the algorithms."""

from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Node:
    """Simple graph node.

    Attributes
    ----------
    id : int
        Identifier for the node (1-indexed).
    name : str, optional
        Optional label for the node.
    node_edges : list[int]
        Indices of incident edges in the ``Edge`` array.
    """

    id: int
    name: Optional[str] = None
    node_edges: List[int] = field(default_factory=list)
