import os
import pickle

from collections import defaultdict

from graph import Node, Edge

def check_all_nodes_present(visited_edges, cities_to_visit):
    visited_nodes = [edge.to_node for edge in visited_edges]

    return len(visited_nodes) == cities_to_visit + 1


def get_sum(edges):
    return sum(e.cost for e in edges)

best_score = 0
best_solution = []


class ANT:
    def __init__(self, MaxCost):
        self.MaxCost = MaxCost
        self.visited_edges = []

    def walk(self, start_city, end_city, cities_to_visit):
        current_city = start_city
        current_edge = None

        while not check_all_nodes_present(self.visited_edges, cities_to_visit):
            current_edge = current_city.roulette_wheel(self.visited_edges, start_city, end_city, cities_to_visit)
            current_city = current_edge.to_node

            self.visited_edges.append(current_edge)

    def pheromones(self):
        current_cost = get_sum(self.visited_edges)

        if current_cost < self.MaxCost:
            # Score function
            score = 1000 ** (1 - float(current_cost) / self.MaxCost)

            global best_score
            global best_edges

            if score > best_score:
                best_score = score
                best_edges = self.visited_edges

            for edge in best_edges:
                edge.pheromones += score


def evaporate(all_edges):
    for edge in all_edges:
        edge.pheromones *= 0.99


def check_all_edges(all_edges):
    for edge in all_edges:
        edge.check_pheromones()


def runner(MaxCost, edges, start_node, end_node, cities_to_visit, runs, info=False):

    low_count = 0
    lowest_cost = MaxCost
    highest_cost = 0

    #shortest_path = []
    distances = []

    for path in range(runs):
        evaporate(edges)

        ant = ANT(MaxCost)
        ant.walk(start_node, end_node, cities_to_visit)
        ant.pheromones()
        check_all_edges(edges)

        cost = get_sum(ant.visited_edges)
        distances.append(cost)

        if cost > highest_cost:
            highest_cost = cost

        if cost < lowest_cost:
            lowest_cost = cost
            low_count = 1

        if cost == lowest_cost:
            low_count += 1

        if low_count == 10000:
            break

        print("Run #", path) if path % (runs / 10) == 0 and not info else None
        print("Run #", path, "~ path cost:", cost) if info else None

    print("\nLowest detected cost: ", lowest_cost, " (", low_count, ")", "\nHighest detected cost: ",
          highest_cost) if info else None

    # Print the best path detected
    ant = ANT(MaxCost)
    ant.walk(start_node, end_node, cities_to_visit)

    print("\nBest Found Path: (Cost: {})".format(get_sum(ant.visited_edges)))

    for edge in ant.visited_edges:
        print(" ", edge, "~ Pheromones:", edge.pheromones)

    return ant.visited_edges, distances


def search_for_shortest_path(graph, starting_city, ending_city, cities_to_visit):
    nodes, edges, nodes_names = pickle.load(open(os.path.join('data', graph), 'rb'))

    MaxCost = get_sum(edges)

    path, results = runner(MaxCost, edges, nodes_names[starting_city], nodes_names[ending_city], cities_to_visit, 50000)

    return [path, results]


if __name__ == '__main__':
    tests = [('Bergen', 'Stavanger', 1),('Stavanger', 'Bergen', 1)]

    test_results = defaultdict(list)

    for test in tests:
        result = search_for_shortest_path('norway_graph.p', 'Bergen', 'Stavanger', 1)
        test_results[test] = result

    result_path = os.path.join('results', 'MMAS')
    print(result_path)

    if not os.path.exists(result_path):
        os.makedirs(result_path)

    pickle.dump(test_results, open(os.path.join(result_path, 'results.p'), 'wb'))