class DFS:
    def __init__(self, graph, isDirected = False):
        self.isDirected = isDirected
        self.graph = graph
        self.n_vertex = len(graph)
        self.time = 0
        self.parent = [-1] * self.n_vertex
        self.visited = ["WHITE"] * self.n_vertex
        self.discovery = [0] * self.n_vertex
        self.finish = [0] * self.n_vertex
        self.low = [0] * self.n_vertex
        self.edge_type = []
        self.articulation_points = set()
        self.isCyclic = False
        self.current_scc = []
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

    def dfs(self):
        root_call_count = 0
        for vertex in self.graph:
            if self.visited[vertex] == "WHITE":
                self.dfs_visit(vertex, isRoot = True)
                root_call_count += 1
        return root_call_count == 1

    def dfs_visit(self, vertex, isRoot = False):
        self.visited[vertex] = "GRAY"
        self.time += 1
        self.discovery[vertex] = self.time
        self.low[vertex] = self.time
        children = 0
        for neighbor in self.graph[vertex]:

            if self.visited[neighbor] == "WHITE": #tree edge
                children += 1
                self.parent[neighbor] = vertex
                self.edge_type.append((vertex, neighbor, "tree"))
                self.dfs_visit(neighbor, isRoot = False)
                self.low[vertex] = min(self.low[vertex], self.low[neighbor])
                if not isRoot and self.low[neighbor] >= self.discovery[vertex]: 
                    #this neighbor is not connected to grand parents of current vertex at all!
                    #so removing vertex will end up having neighbor totally disconnected
                    self.articulation_points.add(vertex)
                
            elif self.visited[neighbor] == "GRAY":
                if not self.isDirected and neighbor != self.parent[vertex]:
                    self.low[vertex] = min(self.low[vertex], self.discovery[neighbor])
                    self.edge_type.append((vertex, neighbor, "backward"))
                    self.isCyclic = True
                elif self.isDirected:
                    self.edge_type.append((vertex, neighbor, "backward"))
                    self.isCyclic = True

            else: #self.visited[neighbor] == "BLACK"
                if self.isDirected:
                    if self.discovery[vertex] > self.discovery[neighbor]:
                        self.edge_type.append((vertex, neighbor, "cross"))
                    elif self.discovery[vertex] < self.discovery[neighbor]:
                        self.edge_type.append((vertex, neighbor, "forward"))
        
        if isRoot and children > 1:
            self.articulation_points.add(vertex)

        self.time += 1
        self.finish[vertex] = self.time
        self.visited[vertex] = "BLACK"
    
    def find_SCC(self, graph, vertex):
        self.visited[vertex] = "GRAY"
        self.current_scc.append(vertex)
        for neighbor in graph[vertex]:
            if self.visited[neighbor] == "WHITE":
                self.find_SCC(graph, neighbor)
        self.visited[vertex] = "BLACK"

def transpose_graph(graph):
    transposed = {v: [] for v in graph}
    for u in graph:
        for v in graph[u]:
            transposed[v].append(u)
    return transposed

def kosaraju(graph):
    n_vertex = len(graph)
    dfs1 = DFS(graph, isDirected = True)
    dfs1.dfs()

    transposed = transpose_graph(graph)
    print(transposed)
    descending_finish = sorted(range(n_vertex), key= lambda v: dfs1.finish[v], reverse=True)

    dfs2 = DFS(graph, isDirected = True)
    sccs = []

    for v in descending_finish:
        if dfs2.visited[v] == "WHITE":
            dfs2.current_scc = []
            dfs2.find_SCC(transposed, v)
            sccs.append(dfs2.current_scc)
    return sccs

if __name__ == "__main__":

    directed_graph = {
    0: [3],
    1: [0,5],
    2: [6],
    3: [1, 2],
    4: [],
    5: [0],
    6: [2, 4]
    }

    '''
    undirected_graph = {
    0: [1, 5],
    1: [0,2,4],
    2: [1, 3, 4],
    3: [2, 4],
    4: [1, 2, 3],
    5: [0, 6, 7],
    6: [5, 7],
    7: [5, 6]
    }
    '''
    #========================================= INPUT =========================================================
    n_vertex = len(directed_graph)
    dfs_obj = DFS(directed_graph, True) #graph, boolean isDirected
    isConnected = dfs_obj.dfs()
    #=========================================================================================================
    print(f"Graph is connected? {isConnected}")
    print(f"Graph is cyclic? {dfs_obj.isCyclic}")
    #print(dfs_obj.discovery)
    #print(dfs_obj.finish)
    print("Discovery and finish times:")
    print({v: (dfs_obj.discovery[v], dfs_obj.finish[v]) for v in range(0, n_vertex)})

    #print(dfs_obj.visited) #make sure that there is not any vertex left unvisited
    print("Parents:") #-1 means root
    print({v: dfs_obj.parent[v] for v in range(0, n_vertex)})
    print("Edge types:")
    print(dfs_obj.edge_type)

    if dfs_obj.isDirected:
        print(f'Strongly Connceted Components: {kosaraju(directed_graph)}')

    if not dfs_obj.isDirected:
        print("Articulation Points:")
        print(dfs_obj.articulation_points)
        print("Low times:") 
        #oldest time that each vertex have access; used for finding articulation points
        print({v: dfs_obj.low[v] for v in range(0, n_vertex)})

    if dfs_obj.isDirected and not dfs_obj.isCyclic:
        finish_dict = {v: dfs_obj.finish[v] for v in range(n_vertex)}
        sorted_vertices = sorted(finish_dict, key = lambda v: finish_dict[v], reverse=True)
        print("Topological Order:")
        print(sorted_vertices)