import math
from .DFS import *
from .FiboHeap import FibonacciHeap

class Prim_FiboHeap:
    def __init__(self, graph):
        self.graph = graph
        self.vertices = set(graph) | {v for u in self.graph for v in self.graph[u]}
        self.n_vertex = len(self.vertices) 
        self.parent = {u:None for u in graph}
        self.distance = {}
        self.fheap = FibonacciHeap()
        # Maps each vertex to its corresponding Fibonacci heap node,
        # so we can perform efficient decrease_key operations.
        self.handles = {} 
        # to know which vertices are still in queue
        self.in_queue = set() 
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
    
    def _validate_undirected(self):
        for u in self.graph:
            for v in self.graph[u]:
                if u not in self.graph.get(v, {}):
                    raise ValueError(f"This graph is not properly undirected: missing edge {v} : {u}")
   
    def run(self, start):
        if start not in self.vertices:
            raise ValueError("start vertex not in graph")
        for u in self.vertices:
            if u == start:
                self.distance[start] = 0
                self.handles[start] = self.fheap.insert(0, start)
                self.in_queue.add(u)
            else:
                self.distance[u] = math.inf
                self.handles[u] = self.fheap.insert(math.inf, u)
                self.in_queue.add(u)
                
        while not self.fheap.is_empty():
            node_u = self.fheap.extract_min()
            u = node_u.value
            self.in_queue.remove(u)
            for v in self.graph[u]:
                if v in self.in_queue and self.graph[u][v] < self.distance[v]:
                    self.parent[v] = u
                    self.distance[v] = self.graph[u][v]
                    self.fheap.decrease_key(self.handles[v], self.graph[u][v])

        mst = [(v, self.parent[v], self.distance[v]) for v in self.vertices if self.parent[v] is not None]
        cost = sum(self.distance.values())
        return mst, cost        

if __name__ == "__main__":
    
    undirected_weighted_graph_0 = {
    'a': {'b':9, 'e':8, 'f':5},
    'b': {'a':9, 'c':11, 'e':10},
    'c': {'b':11,'e':3,'d':2},
    'd': {'e':4,'c':2},
    'e': {'a':8, 'b':10, 'c':3, 'f':7, 'd':4},
    'f': {'a':5, 'e':7}
    }

    start = 'a'
    prim_obj = Prim_FiboHeap(undirected_weighted_graph_0)
    mst, cost = prim_obj.run(start)
    print(f'minimum spanning tree: {mst}')
    print(f'Total cost: {cost}')
    
    
