#it works for both directed and undirected graphs
#for undirected graphs, for each edge you have to define the edge and its reverse
import math
class Matrix_Squaring:
    def __init__(self, graph):
        self.graph = graph
        self.vertices = sorted(set(graph) | {v for u in self.graph for v in self.graph[u]})
        self.idx = {v: i for i, v in enumerate(self.vertices)}
        self.idx_reverse = {i: v for v,i in self.idx.items()} 
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
        for _ in range(math.ceil(math.log2(self.n_vertex-1))):
            new_W = [[math.inf] * self.n_vertex for _ in range(self.n_vertex)]
            new_P = [[None] * self.n_vertex for _ in range(self.n_vertex)]
            for v in range(self.n_vertex):
                for i in range(self.n_vertex):
                    minimum = self.W[v][i]
                    parent = self.P[v][i]
                    for j in range(self.n_vertex):
                        if self.W[v][j] != math.inf and self.W[j][i] != math.inf:
                            temp = self.W[v][j] + self.W[j][i]
                            if temp < minimum:
                                minimum = temp
                                parent = self.P[j][i] if self.P[j][i] is not None else j
                    new_W[v][i] = minimum
                    new_P[v][i] = parent
            self.W, self.P = new_W, new_P

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
        i, j = self.idx[start], self.idx[target]
        if self.P[i][j] is None:
            return [start, target] if start != target else [start]
        k = self.idx_reverse[self.P[i][j]]
        return self.get_shortest_path(start, k)[:-1] + self.get_shortest_path(k, target)

if __name__ == "__main__":
    
    #start from 1
    directed_weighted_graph_0 = {
    1: {2:5},
    2: {1:50, 3:15, 4:5},
    3: {1:30, 4:15},
    4: {1:15, 3:5}
    }

    matrix_squaring_obj = Matrix_Squaring(directed_weighted_graph_0)
    matrix_squaring_obj.run()
    print(f'Weight matrix: {matrix_squaring_obj.W}')
    print(f'Path matrix: {matrix_squaring_obj.P}')
    print(f'Graph contains negative cycle? {matrix_squaring_obj.check_negative_cycle()}')

    start, target = 1, 3
    print(f'path: {matrix_squaring_obj.get_shortest_path(start, target)}')
    print(f'path cost is: {matrix_squaring_obj.W[matrix_squaring_obj.idx[start]][matrix_squaring_obj.idx[target]]}')
