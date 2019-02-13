import os
import pickle
from pprint import pprint
import csv

def extract_information(row, countries):
    """
    Extraction relevant information from row of data, based on list of countries.

    Relevant information is:
        International name
        Longitude and latitude
        Population
    """
    native, international, longitude, latitude, population, country, code_2, code_3, region = row

    if str(country) in countries:
        return [str(international), float(longitude), float(latitude), int(float(population))]

    return None

def read_csv_file(folder, filename, countries):
    """
    Reading relevant information from csv-file based on list of countries,
    sorting the result based on the population of the cities.
    """

    path = os.path.join(folder, filename)
    data = []

    with open(path, encoding="utf8") as csv_file:
        file_reader = csv.reader(csv_file)

        for row in file_reader:
            row_info = extract_information(row, countries)

            if row_info:
                data.append(row_info)

    return sorted(data, key=lambda x: x[-1], reverse=True)


def create_dataset(folder, input_file, output_file, countries):
    """
    Creating the dataset needed for the creation of the graph used by the Ant Colony Optimization.
    """
    dataset = read_csv_file(folder, input_file, countries)
    pprint(dataset)

    pickle.dump(dataset, open(os.path.join(folder, output_file), 'wb'))


if __name__ == "__main__":
    create_dataset(folder='data', input_file='world_cities.csv', output_file='norwegian_cities.p', countries=['Norway'])