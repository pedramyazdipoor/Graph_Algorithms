from .FiboHeap import FibonacciHeap
#it works for both directed and undirected graphs
#for undirected graphs, for each edge you have to define the edge and its reverse
class Dijkstra:
    def __init__(self, graph):
        self.graph = graph
        self.vertices = set(graph) | {v for u in self.graph for v in self.graph[u]}
        self.n_vertex = len(self.vertices)
        self.start = None
        self._reset()

    #reset parents and distances and priority queue; so run() is callable over and over
    def _reset(self):
        self.parent = {u:None for u in self.vertices}
        self.distance = {u:float('inf') for u in self.vertices}
        #self.fheap = makefheap()
        self.fheap = FibonacciHeap()
        self.handles = {}
    
    def _relax(self, edge):
        u, v, w = edge
        if self.distance[v] > self.distance[u] + w:
            self.distance[v] = self.distance[u] + w
            self.parent[v] = u
            if v in self.handles:
                self.fheap.decrease_key(self.handles[v], self.distance[v])
            else:
                self.handles[v] = self.fheap.insert(self.distance[v], v)
            #fheappush(self.fheap, (self.distance[v], v))

    def run(self, start):
        if start not in self.vertices:
            raise ValueError("start vertex not in graph")
        for u in self.graph:
            for v in self.graph[u]:
                if self.graph[u][v] < 0:
                    raise ValueError("there is an edge with negative weight")
        self._reset()
        self.start = start
        self.distance[start] = 0
        self.handles[start] = self.fheap.insert(0, start)
        #fheappush(self.fheap, (0, start))
        
        #while self.fheap.num_nodes > 0:
        while not self.fheap.is_empty():
            #pr_u, u = fheappop(self.fheap)
            node_u = self.fheap.extract_min()
            u = node_u.value
            #if pr_u != self.distance[u]:
                #continue
            for v in self.graph[u]:
                self._relax((u, v, self.graph[u][v]))
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
        

if __name__ == "__main__":
    
    directed_weighted_graph_0 = {
    's': {'t':10, 'y':5},
    't': {'x':1, 'y':2},
    'y': {'x':9,'t':3, 'z':2},
    'x': {'z':4},
    'z': {'s':7, 'x':6}
    }

    start, target = 's', 'x'
    dijkstra_obj = Dijkstra(directed_weighted_graph_0)
    distance, parent = dijkstra_obj.run(start)
    print(f'distances: {distance}')
    print(f'parents: {parent}')
    cost, path = dijkstra_obj.get_shortest_path(target)
    print(f"shortest path: {path}")
    print(f"shortest path cost: {cost}")