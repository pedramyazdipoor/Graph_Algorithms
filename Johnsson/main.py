from algorithms.Johnsson import Johnsson

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
    print(f"Weight matrix: {johnsson_obj.run()}")
    print(f"Shortest path from {start} to {target}: {johnsson_obj.get_shortest_path(start, target)}")
