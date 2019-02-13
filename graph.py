import os
import pickle
import random
from math import radians, cos, sin, asin, sqrt
import operator as op
import functools

MaxPheromones = 100000
MinPheromones = 1


class Node:
    def __init__(self, city_name, longitude, latitude):
        self.city_name = city_name
        self.longitude = longitude
        self.latitude = latitude
        self.edges = []

    def roulette_wheel(self, visited_edges, start_node, end_node, cities_to_visit):
        visited_nodes = [edge.to_node for edge in visited_edges]

        if len(visited_nodes) == cities_to_visit:
            viable_edges = [edge for edge in self.edges if edge.to_node == end_node]
        else:
            viable_edges = [edge for edge in self.edges if
                            edge.to_node not in visited_nodes and edge.to_node != start_node and edge.to_node != end_node]

        if not viable_edges:
            viable_edges = [edge for edge in self.edges if edge.to_node not in visited_nodes]

        random.shuffle(viable_edges)

        max_value = sum([edge.pheromones for edge in viable_edges])
        rand_value = random.uniform(0, max_value)

        pointer = 0

        for edge in viable_edges:
            if pointer + edge.pheromones > rand_value:
                return edge
            pointer += edge.pheromones

    def __repr__(self):
        return self.city_name


class Edge:
    def __init__(self, from_node, to_node, cost):
        self.from_node = from_node
        self.to_node = to_node
        self.cost = cost
        self.pheromones = 100000

    def check_pheromones(self):
        if self.pheromones > MaxPheromones:
            self.pheromones = MaxPheromones

        if self.pheromones < MinPheromones:
            self.pheromones = MinPheromones

    def __repr__(self):
        return self.from_node.city_name + "--(" + str(self.cost) + ")--" + self.to_node.city_name


def haversine(longitude_1, latitude_1, longitude_2, latitude_2):
    """
    Calculate the great circle distance between two points on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    longitude_1, latitude_1, longitude_2, latitude_2 = map(radians, [longitude_1, latitude_1, longitude_2, latitude_2])

    # haversine formula
    d_longitude = longitude_2 - longitude_1
    d_latitude = latitude_2 - latitude_1

    a = sin(d_latitude / 2) ** 2 + cos(latitude_1) * cos(latitude_2) * sin(d_longitude / 2) ** 2
    c = 2 * asin(sqrt(a))

    km = 6367 * c

    return km


def nCr(n, r):
    r = min(r, n - r)

    if r == 0:
        return 1

    numerator = functools.reduce(op.mul, range(n, n - r, -1))
    denominator = functools.reduce(op.mul, range(1, r + 1))

    return numerator // denominator


def create_graph(folder, input_file, output_file):
    """
    Creating graph, containing the distance between city nodes, for the Ant Colony to traverse.
    """
    input_path = os.path.join(folder, input_file)
    output_path = os.path.join(folder, output_file)

    cities = pickle.load(open(input_path, "rb"))
    nodes = [Node(i[0], i[1], i[2]) for i in cities]
    edges = []
    name_dict = {}

    number_of_edges = 2 * nCr(len(cities), 2)
    counter = 0

    print("Expected number of edges", number_of_edges)

    for start_index, from_city in enumerate(nodes):
        for pointer in range(start_index + 1, len(nodes)):
            to_city = nodes[pointer]

            from_longitude, from_latitude = from_city.longitude, from_city.latitude
            to_longitude, to_latitude = to_city.longitude, to_city.latitude

            distance = int(haversine(from_longitude, from_latitude, to_longitude, to_latitude))

            e = Edge(from_city, to_city, distance)
            e_inverse = Edge(to_city, from_city, distance)

            edges.append(e)
            edges.append(e_inverse)

            from_city.edges.append(e)
            to_city.edges.append(e_inverse)

        name_dict[from_city.city_name] = from_city

    print("Number of edges", len(edges))
    print("Number of nodes", len(nodes))

    graph = [nodes, edges, name_dict]
    pickle.dump(graph, open(output_path, "wb"))


if __name__ == "__main__":
    create_graph(folder='data', input_file='norwegian_cities.p', output_file='norway_graph.p')
