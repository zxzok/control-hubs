"""Example script demonstrating the Python API."""

from control_package import NodeClassification, FindSensitiveControlHub, ControlSchemes

try:
    import networkx as nx  # type: ignore
except Exception:  # pragma: no cover
    nx = None


def main():
    """Run classification and scheme search on the sample network."""

    input_file = "./net/sample_network.net"

    # usage with .net file
    NodeClassification(input_file)
    FindSensitiveControlHub(input_file)
    ControlSchemes(input_file)

    # alternatively load using networkx if available
    if nx is not None:
        g = nx.DiGraph()
        g.add_edge(1, 2)
        g.add_edge(1, 4)
        g.add_edge(3, 2)
        g.add_edge(4, 3)
        g.add_edge(4, 5)
        ControlSchemes(graph=g, output_file="./result/scheme_from_nx.txt")


if __name__ == "__main__":
    main()
