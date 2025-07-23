from algorithms.dag import Dag

if __name__ == "__main__":
    
    directed_weighted_graph_0 = {

    'w': {'s':-3, 'x':-4},
    's': {'x':4, 'y':3, 'z':5},
    'y': {'z':-1},
    'x': {'y':-2,'z':-1},
    'z': {}
    }

    start, target = 's', 'z'
    dag_obj = Dag(directed_weighted_graph_0)
    distance, parent = dag_obj.run(start)
    print(f'distances: {distance}')
    print(f'parents: {parent}')

    cost, path = dag_obj.get_shortest_path(target)
    print(f"shortest path: {path}")
    print(f"shortest path cost: {cost}")