from .DFS import DFS

class Kruskal:
    def __init__(self, graph):
        self.graph = graph
        self.n_vertex = len(graph)
        self.rank = {u: 0 for u in graph}  
        self.mst = [] #minimum spanning tree
        self.parent = {u:u for u in graph}
        self.edges = self._listEdges()
        self.cost = 0
        self._validate_undirected()
        if not self._isconnected():
            raise ValueError("There is no MST because the graph is not connected")
    
    #run dfs once. if dfs_visit gets called more than once it means there is a vertex which is not 
    #accessible from start vertex
    def _isconnected(self):
        index_map = {v:i for i,v in enumerate(self.graph)}
        int_graph = {index_map[u]: [index_map[v] for v in self.graph[u]] for u in self.graph}
        dfs_obj = DFS(int_graph, False) #graph, boolean isDirected
        isConnected = dfs_obj.dfs()
        return isConnected

    # MST is only for undirected graphs
    def _validate_undirected(self):
        for u in self.graph:
            for v in self.graph[u]:
                if u not in self.graph.get(v, {}):
                    raise ValueError(f"This graph is not properly undirected: missing edge {v} : {u}")

    #collect all edges of graph and sort them by weight
    def _listEdges(self):
        processed_edges, edges = set(), []
        for u in self.graph:
            for v in self.graph[u]:
                edge = tuple(sorted((u,v)))
                if edge not in processed_edges:
                    processed_edges.add(edge)
                    edges.append((edge[0], edge[1], self.graph[u][v]))
        edges.sort(key = lambda x: x[2]) #sort edges by weight
        return edges
    
    #find root of each vertex recursively
    def find(self, x):
        if self.parent[x] == x:
            return x
        self.parent[x] = self.find(self.parent[x]) #path compression
        return self.parent[x]
    
    #best approach is to choose the deeper root, so if a vertex is chosen, its rank increments by 1 
    #choosing deeper root let us make find(x) faster because one root will be parent of more vertices and 
    #helps us keep the tree of parents shallower
    def union(self, x, y):
        root_x, root_y = self.find(x), self.find(y)
        if root_x == root_y:
            return False
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        return True
    
    #choose an edge keep in mind there must be no cycle! so if root parent of two vertices are the same
    #donot add that edge
    def doKruskal(self):
        for u,v,w in self.edges:
            if self.union(u,v) :
                self.mst.append((u,v,w))
                self.cost += w
        return self.mst, self.cost



    

    