import os

from matplotlib import pyplot as plt
import glob
import pickle

from graph import Node, Edge


def plot_shortest_path(test_data, result, output_folder, nodes):
    starting_city, ending_city, to_visit = test_data

    name = f'{starting_city}_{ending_city}_{to_visit}'

    city_x_values = [n.latitude for n in nodes]
    city_y_values = [n.longitude for n in nodes]

    plt.plot(city_x_values, city_y_values, 'ro')

    path, results = result
    path_x_values = [path[0].from_node.latitude] + [n.to_node.latitude for n in path]
    path_y_values = [path[0].from_node.longitude] + [i.to_node.longitude for i in path]

    plt.plot(path_x_values, path_y_values)

    plt.title(f'{name}: {sum([i.cost for i in path])} km')

    plt.ylim([56, 72])
    plt.xlim([0, 35])

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    plt.savefig(os.path.join(output_folder, f'{name}.png'))
    plt.clf()


if __name__ == '__main__':
    graph = 'norway_graph.p'

    nodes, _, _ = pickle.load(open(os.path.join('data', graph), 'rb'))

    algorithms = ['evaporation', 'MMAS']

    for algorithm in algorithms:
        test_results = pickle.load(open(os.path.join('results', algorithm, 'results.p'), 'rb'))

        for key, value in test_results.items():
            plot_shortest_path(key, value, os.path.join('images', algorithm), nodes)
