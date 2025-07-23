from algorithms.Prim_fiboHeap import Prim_FiboHeap
from algorithms.Prim_minHeap import Prim_minHeap

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
    
    prim_fiboheap_obj = Prim_FiboHeap(undirected_weighted_graph_0)
    mst, cost = prim_fiboheap_obj.run(start)
    print(f'minimum spanning tree: {mst}')
    print(f'Total cost: {cost}')

    prim_minheap_obj = Prim_minHeap(undirected_weighted_graph_0)
    mst, cost = prim_minheap_obj.run(start)
    print(f'minimum spanning tree: {mst}')
    print(f'Total cost: {cost}')
    