import argparse
import hypermax.cui
import json
import time
import os.path
import hyperopt
from pprint import pprint
from hypermax.optimizer import Optimizer
import csv

def main():
    parser = argparse.ArgumentParser(description='Provide configuration options for Hypermax')
    parser.add_argument('configuration_file', metavar='configuration_file', type=argparse.FileType('rb'), nargs=1, help='The JSON based configuration file which is used to configure the hyper-parameter search.')
    parser.add_argument('results_directory', metavar='results_directory', type=str, nargs='?', help='The directory of your existing results to reload and restart from.')

    args = parser.parse_args()

    with args.configuration_file[0] as file:
        config_data = json.load(file)

    optimizer = Optimizer(config_data)

    if args.results_directory:
        with open(os.path.join(args.results_directory, 'results.csv')) as file:
            reader = csv.DictReader(file)
            results = list(reader)
            for result in results:
                for key,value in result.items():
                    if value:
                        try:
                            if '.' in value:
                                result[key] = float(value)
                            else:
                                result[key] = int(value)
                        except ValueError:
                            result[key] = value
                    elif key == 'loss':
                        result[key] = None
                    elif key in optimizer.resultInformationKeys:
                        result[key] = ''
                    else:
                        result[key] = None
            optimizer.results = results


    optimizer.runOptimization()

    hypermax.cui.launchHypermaxUI(optimizer)