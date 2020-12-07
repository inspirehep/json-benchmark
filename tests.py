import csv

import functools

import json
import orjson
import rapidjson
import simplejson
import timeit
import ujson

import os


def test_files(path):
    results = []
    jsons=[json, orjson, ujson, rapidjson, simplejson]
    (dirpath, dirnames, filenames) = next(os.walk(path))
    for filename in filenames:
        with open(f"{dirpath}/{filename}", 'r') as file:
            data = file.read()
            print(f"file: {filename} - loads, dumps")
            results_partial = {"file": filename}
            for json_lib in jsons:
                json_load, json_dump = benchmark(data, json_lib)
                print(f"{json_lib.__name__}: {json_load}, {json_dump}")
                results_partial[f"{json_lib.__name__}_load"] = json_load
                results_partial[f"{json_lib.__name__}_dump"] = json_dump
            results.append(results_partial)
    with open("results.json", "w") as output:
        json.dump(results, output)
    with open('results.csv', 'w') as output:
        csv_file = csv.DictWriter(output, results[0].keys(), delimiter=';')
        csv_file.writeheader()
        for row in results:
            csv_file.writerow(row)


def benchmark(data, json_lib):
    load_json = timeit.Timer(functools.partial(json_lib.loads, data), setup=f"import {json_lib.__name__}").timeit(100)
    json_data = json_lib.loads(data)
    dump_json = timeit.Timer(functools.partial(json_lib.dumps, json_data), setup=f"import {json_lib.__name__}").timeit(100)
    return load_json, dump_json


test_files("data")
