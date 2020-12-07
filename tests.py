from collections import defaultdict
from statistics import quantiles

import csv

import functools

import json
import orjson
import rapidjson
import simplejson
import timeit
import ujson

import os

jsons = [json, orjson, ujson, rapidjson, simplejson]


def test_files(path):
    results = []
    (dirpath, dirnames, filenames) = next(os.walk(path))
    for filename in filenames:
        results.append(process_file(dirpath, filename))
    #Not storing results anymore

def store_results(results):
    with open("results.json", "w") as output:
        json.dump(results, output)
    with open('results.csv', 'w') as output:
        csv_file = csv.DictWriter(output, results[0].keys(), delimiter=';')
        csv_file.writeheader()
        for row in results:
            csv_file.writerow(row)


def process_file(dirpath, filename):
    with open(f"{dirpath}/{filename}", 'r') as file:
        data_lines = file.readlines()
        print(f"file: {filename}:")
        partial_results = process_file_lines(filename, data_lines)

        stats = produce_stats(partial_results)
        print(stats)

        return stats


def produce_stats(partial_results):
    summary = {}
    for key, values in partial_results.items():
        min_value = min(values)
        max_value = max(values)
        avg_value = sum(values) / len(values)
        quants = quantiles(values, n=100)
        summary[key] = {'min': min_value, 'max': max_value, 'avg': avg_value,
                        'p5': quants[4], 'p25': quants[24], 'p50': quants[49], 'p75': quants[74],
                        'p95': quants[94]}
    return summary

def process_file_lines(filename, data_lines):
    results_partial = defaultdict(list)
    for data in data_lines:
        for json_lib in jsons:
            json_load, json_dump = benchmark(data, json_lib)
            results_partial[f"{json_lib.__name__}_load"].append(json_load)
            results_partial[f"{json_lib.__name__}_dump"].append(json_dump)
    return results_partial


def benchmark(data, json_lib):
    load_json = timeit.Timer(functools.partial(json_lib.loads, data), setup=f"import {json_lib.__name__}").timeit(5)
    json_data = json_lib.loads(data)
    dump_json = timeit.Timer(functools.partial(json_lib.dumps, json_data), setup=f"import {json_lib.__name__}").timeit(5)
    return load_json, dump_json


test_files("data")
