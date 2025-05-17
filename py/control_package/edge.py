"""Edge representation for internal graph structure."""

from dataclasses import dataclass

@dataclass
class Edge:
    """Directed edge between ``src`` and ``des`` nodes."""

    src: int
    des: int
