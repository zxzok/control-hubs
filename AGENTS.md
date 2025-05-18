# AGENT instructions for control-hubs repository

## Overview
This repository implements algorithms to find **control hubs** in directed networks.
Nodes are categorized as **Head**, **Tail**, or **Control Hub**. The Python
implementation (`py/control_package/node_classification.py`) uses a bipartite
representation and Hopcroft--Karp search.

## Node classification workflow
1. Load the network from a `.net` file or `networkx` graph.
2. Split each node `v` into `nodeSrc[v]` and `nodeDes[v]` to build a bipartite
   graph. All edges go from a `nodeSrc` node to a `nodeDes` node.
3. Execute BFS/DFS from the source side (`BFS_APU`/`DFS_APU`) to find unmatched
   source nodes. These nodes form the **Tail** set.
4. Reinitialize and repeat the search from the destination side
   (`BFS_APD`/`DFS_APD`) to find unmatched destination nodes. These nodes form the
   **Head** set.
5. Any node not in `Head` or `Tail` is labeled as a **Control Hub**.

## Agent guidelines
- When modifying files under `py/` or `src/`, run the demo script to ensure the
  code executes without errors:
  
  ```bash
  PYTHONPATH=py python3 py/main/demo.py
  ```
  The script writes results to the `result/` directory.
- Use snake_case for Python identifiers and include docstrings for new
  functions.
- Keep Java code consistent with existing formatting.
- Preserve the BFS/DFS structure in `NodeClassification` when editing the
  algorithm.
- Commit messages must be in English and summarize the change.
