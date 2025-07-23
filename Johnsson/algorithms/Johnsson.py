from .Bellman_Ford import *
from .Dijkstra_fiboheap import *

class Johnsson:
    def __init__(self, graph):
        self.graph = graph
        self.vertices = sorted(set(graph) | {v for u in self.graph for v in self.graph[u]})
        self.idx = {v: i for i, v in enumerate(self.vertices)}
        self.n_vertex = len(self.vertices)
        self.h = self._modify_weights()
        self.W, self.P = [], []
        
    
    def _modify_weights(self):
        self.graph['temp_source'] = {}
        for u in self.vertices:
            self.graph['temp_source'][u] = 0 
        #self.vertices.append('temp_source')
        belamn_ford_obj = Bellman_Ford(self.graph)
        distance, parent = belamn_ford_obj.run('temp_source')
        self.graph.pop('temp_source')
        distance.pop('temp_source')
        for i in self.graph:
            for j in self.graph[i]:
                self.graph[i][j] = self.graph[i][j] + distance[i] - distance[j]
        return distance
    
    def run(self):
        dijkstra_obj = Dijkstra(self.graph)
        for i in range(self.n_vertex):
            start = self.vertices[i]
            distance, parent = dijkstra_obj.run(start)
            self.W.append(distance)
            self.P.append(parent)
        for i, u in enumerate(self.W):
            src = self.vertices[i]
            for v in u:
                if u[v] != float('inf'):
                    u[v] = u[v] - self.h[src] + self.h[v]
        return self.W

    #get shortest path from start vertex to any target is possible after calling run() method
    def get_shortest_path(self, start, target):
        #check for validity of start and target vertex
        if start is None:
            raise RuntimeError("You must enter start vertex")
        ind = self.vertices.index(start)
        if target not in self.vertices:
            raise ValueError("target vertex not in graph")
        if self.W[ind][target] == float('inf'):
            raise ValueError("target is not reachable")
        if target == start:
            return [start]
        
        path = []
        current = target
        parent = self.P[ind]
        while current is not None: 
            path.append(current)
            if current == start:
                return self.W[ind][target], path[::-1] #reverse path
            current = parent[current]
        raise ValueError("NO PATH FOUND")

if __name__ == "__main__":
    
    directed_weighted_graph_0 = {
    'a': {'b':3, 'e':-4, 'c':8},
    'b': {'d':1, 'e':7},
    'c': {'b':4},
    'd': {'a':2, 'c':-5},
    'e': {'d':6}
    }

    start, target = 'd', 'c'
    johnsson_obj = Johnsson(directed_weighted_graph_0)
    #print(johnsson_obj.graph)
    print(johnsson_obj.run())
    print(johnsson_obj.get_shortest_path(start, target))
