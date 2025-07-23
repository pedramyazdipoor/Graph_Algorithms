from algorithms.Kruskal import Kruskal

if __name__ == "__main__":
    
    undirected_weighted_graph_0 = {
    'a': {'b':9, 'e':8, 'f':5},
    'b': {'a':9, 'c':11, 'e':10},
    'c': {'b':11,'e':3,'d':2},
    'd': {'e':4,'c':2},
    'e': {'a':8, 'b':10, 'c':3, 'f':7, 'd':4},
    'f': {'a':5, 'e':7}
    }

    kruskal_obj = Kruskal(undirected_weighted_graph_0)
    mst, cost = kruskal_obj.doKruskal()
    print(f'minimum spanning tree: {mst}')
    print(f'Total cost: {cost}')