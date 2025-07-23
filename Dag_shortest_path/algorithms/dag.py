from .DFS import *

class Dag:
    def __init__(self, graph):
        self.graph = graph
        self.vertices = set(graph) | {v for u in self.graph for v in self.graph[u]}
        self.n_vertex = len(self.vertices) 
        self.index_map = {v:i for i,v in enumerate(self.vertices)}
        self.idx = {i: v for i,v in enumerate(self.vertices)}
        self.isDirected = self._validate_directed()
        self.isCyclic, self.topological_order = self._run_dfs()
        if not self.isDirected:
            raise ValueError("This algorithm is only compatible with directed graphs")
        if self.isCyclic:
            raise ValueError("This algorithm is only compatible with acyclic graphs")
        self._reset()

    def _validate_directed(self):
        for u in self.graph:
            for v in self.graph[u]:
                if u not in self.graph.get(v, {}):
                    return True
        return False  

    def _run_dfs(self):
        int_graph = {self.index_map[u]: [self.index_map[v] for v in self.graph[u]] for u in self.graph}
        dfs_obj = DFS(int_graph, self.isDirected) #graph, boolean isDirected
        _ = dfs_obj.dfs()  
        finish_dict = {v: dfs_obj.finish[v] for v in range(self.n_vertex)}
        sorted_vertices = sorted(finish_dict, key = lambda v: finish_dict[v], reverse=True)
        return dfs_obj.isCyclic, sorted_vertices

    def _reset(self):
        self.parent = {u:None for u in self.vertices}
        self.distance = {u:float('inf') for u in self.vertices}
    
    def _relax(self, edge):
        u, v, w = edge
        if self.distance[v] > self.distance[u] + w:
            self.distance[v] = self.distance[u] + w
            self.parent[v] = u
    
    def run(self, start):
        self._reset()
        self.start = start
        if start not in self.vertices:
            raise ValueError("Start vertex does not exist in this graph")
        self.distance[self.start] = 0
        for u in self.topological_order:
            i = self.idx[u]
            for j in self.graph.get(i, {}):
                edge = (i, j, self.graph[i][j])
                self._relax(edge)
        return self.distance, self.parent

    #get shortest path from start vertex to any target is possible after calling run() method
    def get_shortest_path(self, target):
        #check for validity of start and target vertex
        if self.start is None:
            raise RuntimeError("You must run algorithm before getting shortest path")
        if target not in self.vertices:
            raise ValueError("target vertex not in graph")
        if self.distance[target] == float('inf'):
            raise ValueError("target is not reachable")
        if target == self.start:
            return [self.start]
        path = []
        current = target
        while current is not None: 
            path.append(current)
            if current == self.start:
                return self.distance[target], path[::-1] #reverse path
            current = self.parent[current]
        raise ValueError("NO PATH FOUND")


