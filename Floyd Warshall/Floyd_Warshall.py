#it works for both directed and undirected graphs
#for undirected graphs, for each edge you have to define the edge and its reverse
class Floyd_Warshall:
    def __init__(self, graph):
        self.graph = graph
        self.vertices = sorted(set(graph) | {v for u in self.graph for v in self.graph[u]})
        self.idx = {v: i for i, v in enumerate(self.vertices)}
        self.n_vertex = len(self.vertices)
        self.W = [[float('inf')] * self.n_vertex for _ in range(self.n_vertex)]
        self.P = [[None] * self.n_vertex for _ in range(self.n_vertex)]
        self._buildW()

    def _buildW(self):
        for u in self.vertices:
            i = self.idx[u]
            for v in self.vertices:
                j = self.idx[v]
                if u == v:
                    self.W[i][j] = 0
                elif v in self.graph.get(u, {}):
                    self.W[i][j] = self.graph[u][v]
    
    def run(self):
        for k in range(self.n_vertex):
            for u in range(self.n_vertex):
                for v in range(self.n_vertex):
                    if self.W[u][v] > self.W[u][k] + self.W[k][v]:
                        self.W[u][v] = self.W[u][k] + self.W[k][v]
                        self.P[u][v] = self.vertices[k]
    
    def check_negative_cycle(self):
        for i in range(self.n_vertex):
            if self.W[i][i] < 0:
                return True
        return False
    
    def get_shortest_path(self, start, target):
        if start not in self.vertices or target not in self.vertices:
            raise ValueError("start or target vertex donot exist in this graph")
        if self.W[self.idx[start]][self.idx[target]] == float('inf'):
            raise ValueError("no path between start and target")
        if self.P[self.idx[start]][self.idx[target]] is None:
            return [start, target] if start != target else [start]
        k = self.P[self.idx[start]][self.idx[target]]
        return self.get_shortest_path(start, k)[:-1] + self.get_shortest_path(k, target)
            
    def get_transitive_closure(self):
        T = [[False] * self.n_vertex for _ in range(self.n_vertex)]
        for u in self.vertices:
            i = self.idx[u]
            for v in self.vertices:
                j = self.idx[v]
                if u == v or v in self.graph.get(u, {}):
                    T[i][j] = True
        
        for k in range(self.n_vertex):
            for i in range(self.n_vertex):
                for j in range(self.n_vertex):
                    if not T[i][j]:
                        T[i][j] = T[i][k] and T[k][j]
        return T
    
    def get_transitive_closure_usingw(self):
        T = [[False]*self.n_vertex for _ in range(self.n_vertex)]
        for i in range(self.n_vertex):
            for j in range(self.n_vertex):
                if self.W[i][j] < float('inf'):
                    T[i][j] = True
        return T
    
if __name__ == "__main__":
    
    #start from 1
    directed_weighted_graph_0 = {
    1: {2:5},
    2: {1:50, 3:15, 4:5},
    3: {1:30, 4:15},
    4: {1:15, 3:5}
    }

    floyd_warshall_obj = Floyd_Warshall(directed_weighted_graph_0)
    floyd_warshall_obj.run()
    print(f'Weight matrix: {floyd_warshall_obj.W}')
    print(f'Path matrix: {floyd_warshall_obj.P}')
    print(f'Graph contains negative cycle? {floyd_warshall_obj.check_negative_cycle()}')

    start, target = 1, 3
    print(f'path: {floyd_warshall_obj.get_shortest_path(start, target)}')
    print(f'path cost is: {floyd_warshall_obj.W[floyd_warshall_obj.idx[start]][floyd_warshall_obj.idx[target]]}')

    print(f"Transitive Closure Matrix: {floyd_warshall_obj.get_transitive_closure()}")
    print(f"Transitive Closure Matrix Using W: {floyd_warshall_obj.get_transitive_closure_usingw()}")

    