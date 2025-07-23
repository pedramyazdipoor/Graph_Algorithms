from collections import deque
import copy
class Ford_Fulkerson:
    def __init__(self, graph, start, target):
        self.graph = graph
        self.vertices = sorted(set(graph) | {v for u in self.graph for v in self.graph[u]})
        self.n_vertex = len(self.vertices)
        self.residual_graph = copy.deepcopy(graph)
        self.start, self.target = start, target
        self._validate_graph()

    def _validate_graph(self):
        if self.start not in self.vertices or self.target not in self.vertices:
            raise ValueError("Start or target not in graph vertices")
        if self.graph.get(self.target):
            print("Warning: target has out-degree > 0")
        for u in self.graph:
            if self.start in self.graph[u]:
                print("Warning: start has in-degree > 0")
        if not isinstance(self.graph, dict):
            raise TypeError("Graph is not defined as a disctionary")
        for u, neighbors in self.graph.items(): 
            if not isinstance(neighbors, dict):
                raise TypeError(f"Neighbors of vertex {u} have to be in a dictionary")
        for u in self.graph:
            for v in self.graph[u]:
                capacity = self.graph[u][v]
                if not isinstance(capacity, (int, float)) or capacity < 0:
                    raise ValueError(f'Invalid capacity on edge {u} : {v}: {capacity}')
    
    def _bfs(self):
        depth = {u: -1 for u in self.vertices}
        parent = {u: -1 for u in self.vertices}
        visited = {u: False for u in self.vertices}
        searchQ = deque()
        searchQ.append(self.start)
        visited[self.start] = True
        depth[self.start] = 0

        while searchQ:
            vertex = searchQ.popleft()
            for neighbor in sorted(self.residual_graph[vertex]):
                permitted = False
                if neighbor in self.graph[vertex]:
                    remaining_capacity = self.residual_graph[vertex][neighbor]
                    permitted = remaining_capacity > 0

                else:
                    permitted = self.residual_graph[vertex][neighbor] > 0

                if permitted and not visited[neighbor]:
                    searchQ.append(neighbor)
                    visited[neighbor] = True
                    depth[neighbor] = depth[vertex] + 1
                    parent[neighbor] = vertex
        
        return depth, parent
    
    def _get_shortest_path(self, depth, parent):
        if depth[self.target] == -1: #no access to target
            return []
        path = []
        current = self.target
        while current != -1: #current != self.start
            path.append(current)
            current = parent[current]
        return path[::-1] #reverse path
    
    def run(self):
        max_flow = 0
        while True:
            depth, parent = self._bfs()
            path = self._get_shortest_path(depth, parent)
            if not path:
                break  #no augmented path
        
            #minimum of remaining capacity
            bottleneck = min(self.residual_graph[u][v] for u, v in zip(path[:-1], path[1:]))

            #updating residual_graph
            for u, v in zip(path[:-1], path[1:]):
                #increasing flow for edges along the path = decreasing remaining capacity
                self.residual_graph[u][v] -= bottleneck

                #increasing capacity for reverse edge(reversing flow)
                if v not in self.residual_graph:
                    self.residual_graph[v] = {}
                self.residual_graph[v][u] = self.residual_graph[v].get(u, 0) + bottleneck
        
            max_flow += bottleneck
        return max_flow

if __name__ == "__main__":
    
    directed_weighted_graph_0 = {
    's': {'w':16, 'x':13},
    'w': {'y':12},
    'x': {'z':14, 'w':4},
    'y': {'x':9, 't':20},
    'z': {'y':7, 't':4},
    't': {}
    }

    directed_weighted_graph_1 = {
    's': {'a': 10, 'c': 10},
    'a': {'b': 4},
    'c': {'a': 2, 'b': 8},
    'b': {'t': 10},
    't': {}
}

    start, target = 's', 't'
    ford_fulkerson_obj = Ford_Fulkerson(directed_weighted_graph_0, start, target)
    print(f'Maximum flow is: {ford_fulkerson_obj.run()}')
    print(ford_fulkerson_obj.residual_graph)