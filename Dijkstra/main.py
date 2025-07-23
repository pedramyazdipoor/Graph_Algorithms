from algorithms.Dijkstra_fiboHeap import DijkstraFibo
from algorithms.Dijkstra_minHeap import DijkstraMinHeap

if __name__ == "__main__":
    
    directed_weighted_graph_0 = {
    's': {'t':10, 'y':5},
    't': {'x':1, 'y':2},
    'y': {'x':9,'t':3, 'z':2},
    'x': {'z':4},
    'z': {'s':7, 'x':6}
    }

    start, target = 's', 'x'

    dijkstra_obj = DijkstraFibo(directed_weighted_graph_0)
    distance, parent = dijkstra_obj.run(start)
    print(f'distances: {distance}')
    print(f'parents: {parent}')
    cost, path = dijkstra_obj.get_shortest_path(target)
    print(f"shortest path: {path}")
    print(f"shortest path cost: {cost}")

    print()

    dijkstra_obj = DijkstraMinHeap(directed_weighted_graph_0)
    distance, parent = dijkstra_obj.run(start)
    print(f'distances: {distance}')
    print(f'parents: {parent}')
    cost, path = dijkstra_obj.get_shortest_path(target)
    print(f"shortest path: {path}")
    print(f"shortest path cost: {cost}")