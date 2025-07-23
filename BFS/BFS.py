from collections import deque

class BFS:
    def __init__(self, graph, isDirected):
        self.isDirected = isDirected
        self.graph = graph
        self.n_vertex = len(graph)
        self.visited = [False] * self.n_vertex
        self.edge_type = []
        self.processed_edges = set() #just for indirected graphs
        self.depth = [-1] * self.n_vertex 
        self.traversed = []
        self.parent = [-1] * self.n_vertex
        self.isCyclic = False
        self.color = [-1] * self.n_vertex
        self.isBipartite = True
        self.validate_graph()

    def validate_graph(self):
        for vertex in range(self.n_vertex):
            if vertex not in self.graph:
                self.graph[vertex] = []
            for neighbor in self.graph[vertex]:
                if not (0 <= neighbor < self.n_vertex):
                    raise ValueError(f"Neighbor {neighbor} out of range for vertex {vertex}")
                if neighbor not in self.graph:
                    self.graph[neighbor] = []

    def bfs_directed(self, start = 0):
        if not (0 <= start < self.n_vertex):
            raise ValueError(f"vertex start {start} out of range")
        searchQ = deque()
        searchQ.append(start)
        self.visited[start] = True
        self.depth[start] = 0
        self.traversed.append(start)

        while searchQ:
            vertex = searchQ.popleft()
            for neighbor in sorted(self.graph[vertex]):
                if not self.visited[neighbor]:
                    searchQ.append(neighbor)
                    self.visited[neighbor] = True
                    self.traversed.append(neighbor)
                    self.depth[neighbor] = self.depth[vertex] + 1
                    self.parent[neighbor] = vertex
                    self.edge_type.append((vertex, neighbor, "tree"))

                elif self.visited[neighbor]  and self.depth[neighbor] < self.depth[vertex] and self.is_ancestor(vertex, neighbor):
                    self.edge_type.append((vertex, neighbor, "backward"))
                    self.isCyclic = True
                else:
                    self.edge_type.append((vertex, neighbor, "cross"))
    
    def is_ancestor(self, u, v):
        current = u
        while current != -1:
            if current == v:
                return True
            current = self.parent[current]
        return False
                

    def bfs_undirected(self, start = 0):
        if not (0 <= start < self.n_vertex):
            raise ValueError(f"vertex start {start} out of range")
        searchQ = deque()
        searchQ.append(start)
        self.visited[start] = True
        self.depth[start] = 0
        self.traversed.append(start)
        self.color[start] = 0
        while searchQ:
            vertex = searchQ.popleft()
            for neighbor in sorted(self.graph[vertex]):
                edge = tuple(sorted([vertex, neighbor]))
                if edge not in self.processed_edges:
                    if not self.visited[neighbor]:
                        searchQ.append(neighbor)
                        self.visited[neighbor] = True
                        self.traversed.append(neighbor)
                        self.depth[neighbor] = self.depth[vertex] + 1
                        self.parent[neighbor] = vertex
                        self.edge_type.append((vertex, neighbor, "tree"))
                        self.processed_edges.add(edge)
                        self.color[neighbor] = 1 - self.color[vertex]

                    elif neighbor != self.parent[vertex]:
                        self.isCyclic = True
                        self.edge_type.append((vertex, neighbor, "cross"))
                        self.processed_edges.add(edge)
                        if self.color[neighbor] == self.color[vertex]:
                            self.isBipartite = False
                        
                    else:
                        self.edge_type.append((vertex, neighbor, "tree"))
                        self.processed_edges.add(edge)

    def bfs_all_components(self):  
        self.visited = [False] * self.n_vertex
        self.depth = [-1] * self.n_vertex
        self.parent = [-1] * self.n_vertex
        self.color = [-1] * self.n_vertex
        self.isBipartite = True
        self.traversed = []
        self.edge_type = []
        self.processed_edges = set()
        self.isCyclic = False
        root_call_count = 0
        for vertex in range(self.n_vertex):
            if not self.visited[vertex]:
                if self.isDirected:
                    self.bfs_directed(vertex)  
                    
                else:
                    self.bfs_undirected(vertex)
                root_call_count += 1  
        return root_call_count == 1

    def get_shortest_path(self, target):
        if target < 0 or target >= self.n_vertex: #invalid target!
            return []
        elif self.depth[target] == -1: #no access to target
            return []
        path = []
        current = target
        while current != -1: #current != start
            path.append(current)
            current = self.parent[current]
        return path[::-1] #reverse path

if __name__ == "__main__":
    
    directed_graph_1 = {
    0: [1, 2],
    1: [3],
    2: [3, 4],
    3: [5],
    4: [0,1,5],
    5: [6],
    6: [4]
    }

    directed_graph_0 = {
    0: [1, 3],
    1: [2],
    2: [4,5],
    3: [4],
    4: [0,1],
    5: [4]
    }
    
    undirected_graph_0 = {
        0:[1,2],
        1:[0,3],
        2:[0, 3],
        3:[1, 2],
        4: []
    }

    undirected_graph_1 = {
    0: [1,2],
    1: [0,3,4],
    2: [0,3],
    3: [1,2,4],
    4: [1,3,5,7,8],
    5: [4,6],
    6: [5],
    7:[4,8],
    8:[4,7]
    }
    #========================================= INPUT =========================================================
    bfs_obj = BFS(directed_graph_1, True)
    isConnected = bfs_obj.bfs_all_components()
    #=========================================================================================================
    print(f"Graph is connected? {isConnected}")
    print("Edge types:")
    print(bfs_obj.edge_type)
    print("Distances from start:")
    print(bfs_obj.depth)
    print("Traversed vertices:")
    print(bfs_obj.traversed)
    print("Parents:")
    print(bfs_obj.parent)
    print(f"Graph is cyclic? {bfs_obj.isCyclic}")
    if not bfs_obj.isDirected:
        print(f"Graph is bipartite? {bfs_obj.isBipartite}")
        print(bfs_obj.color)  
    print(f"Shortest path to vertex 3: {bfs_obj.get_shortest_path(3)}")
    print(f"Shortest path to vertex 4: {bfs_obj.get_shortest_path(4)}")     
          