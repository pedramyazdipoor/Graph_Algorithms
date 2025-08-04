# 📚 Graph Algorithms in Python

This repository contains my Python implementations of 11 core graph algorithms, each placed in its own directory with modular structure and independent dependencies.

🚀 Implemented Algorithms

DFS (Depth-First Search)
- Discovery & finish time<br>
- Edge classification (tree, back, forward, cross)<br>
- Topological sort<br>
- Articulation points<br>
- Cycle detection<br>
- Strongly connected components

BFS (Breadth-First Search)
- Visitation order<br>
- Edge classification<br>
- Distance from source<br>
- Cycle detection<br>
- Bipartite check (for undirected graphs)<br>
- Shortest path in unweighted graphs

Kruskal’s MST	
- Minimum spanning tree<br>
- Edge list with total cost<br>
- Validates undirectedness & connectivity using DFS

Prim’s MST	
- Implemented with Binary Min-Heap & Fibonacci Heap<br>
- Output comparison included

Dijkstra’s Algorithm	
- Implemented with both Binary Min-Heap & Fibonacci Heap<br>
- No negative edge allowed<br>
- Parent & distance arrays<br>
- Output comparison included

Bellman-Ford Algorithm	
- Handles negative weights<br>
- Detects negative cycles<br>
- Distance & parent arrays<br>
- Path reconstruction

Floyd-Warshall	
- All-pairs shortest paths<br>
- Negative cycle detection<br>
- Path reconstruction<br>
- Transitive closure

Repeated Matrix Squaring	
- Faster all-pairs shortest paths (compared to Floyd)<br>
- Same output except no transitive closure

Johnson’s Algorithm	
- All-pairs shortest paths<br>
- Uses Bellman-Ford for reweighting and Dijkstra with Fibonacci Heap

Ford-Fulkerson	
- Maximum flow using BFS (Edmonds-Karp)<br>
- Residual graph output<br>
- Input validation: no negative capacities, source has no in-edges, sink has no out-edges

Shortest Path in DAGs	
- Validates DAG using DFS<br>
- Topological order for edge relaxation<br>
- Distance & parent arrays<br>
- Supports single-source shortest paths


## 🧠 Design Principles

🧪 Validation: Every algorithm checks for graph validity (e.g. directedness, connectivity, negative weights, source/sink validity).

🧩 Modularity: Each algorithm is in its own folder with separate main.py, helpers, and .gitignore.

⚙ Dependencies: Shared logic (e.g. DFS for SCC or Kruskal) is imported properly. Virtual environments are used in some folders, but excluded from Git.

🧵 Clean Output: Each main file prints relevant data structures (like parent and distance arrays, MST edges and cost, flow/residual graphs) in a readable format.


## 📌 Notes

The Fibonacci heap is implemented manually and optimized for Dijkstra and Prim.

In Johnson’s algorithm, Dijkstra with Fibonacci heap is reused for better asymptotic efficiency.

Some algorithms (like Kruskal, Johnson) rely on helper algorithms (like DFS, Bellman-Ford, Dijkstra).

All code is written in Python 3, and tested on various graph configurations.


## 🧪 How to Run

Navigate to each algorithm folder and if main.py exists run:

python main.py

otherwise run the relevant algorithm.py for each algorithm.


## 📄 License

This project is open-source and free to use for educational or research purposes.
