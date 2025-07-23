#it works for both directed and undirected graphs
#for undirected graphs, for each edge you have to define the edge and its reverse
class Bellman_Ford:
    def __init__(self, graph):
        self.graph = graph
        self.vertices = set(graph) | {v for u in self.graph for v in self.graph[u]}
        self.n_vertex = len(self.vertices)
        self.edges = self._listEdges()
        self.start = None
        self._reset()

    #reset parents and distances so run() is callable over and over
    def _reset(self):
        self.parent = {u:None for u in self.vertices}
        self.distance = {u:float('inf') for u in self.vertices}
    
    #standard relax operation in Bellman-Ford algorithm
    def _relax(self, edge):
        u, v, w = edge
        if self.distance[v] > self.distance[u] + w:
            self.distance[v] = self.distance[u] + w
            self.parent[v] = u
            return True
        return False

    #collect all edges of graph
    def _listEdges(self):
        return [(u, v, self.graph[u][v]) for u in self.graph for v in self.graph[u]]
    
    #for n-1 times: do relax() for each edge in graph
    def run(self, start):
        if start not in self.vertices:
            raise ValueError("start vertex not in graph")
        self._reset()
        self.start = start
        self.distance[start] = 0
        
        for _ in range(0, self.n_vertex-1):
            updated = False
            for edge in self.edges:
                updated |= self._relax(edge)
            if not updated:
                break
        for u, v, w in self.edges:
            if self.distance[v] > self.distance[u] + w:
                raise ValueError("Graph has a negative weight cycle")
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
                return path[::-1] #reverse path
            current = self.parent[current]
        raise ValueError("NO PATH FOUND")
        

if __name__ == "__main__":
    
    directed_weighted_graph_0 = {
    's': {'t':6, 'y':7},
    't': {'x':5, 'y':8, 'z':-4},
    'y': {'x':-3,'z':9},
    'x': {'t':-2},
    'z': {'s':2, 'x':7}
    }

    start, target = 's', 'x'
    belamn_ford_obj = Bellman_Ford(directed_weighted_graph_0)
    print(belamn_ford_obj.edges)
    distance, parent = belamn_ford_obj.run(start)
    print(f'distances: {distance}')
    print(f'parents: {parent}')
    print(f"shortest path: {belamn_ford_obj.get_shortest_path(target)}")
    