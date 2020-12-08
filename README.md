# JSON benchmark with INSPIRE data

## Introduction

Performance of JSON serialization and deserialization in the Python standard library is sometimes slow. Fortunately, there exist several alternative implementations, but their performance depends on the type of data (size, complexity) to be (de)serialized. This is why it's useful to benchmark different libraries on realistic data and on the hardware where they will eventually run. As the [results](#results) show, `orjson` is the clear winner.

Performance of JSON schema validation is also slow, so looking for alternatives there is also useful, but none of them seem satisfactory (see [further](#JSON-schema-validation)).

## What we tested

We tested 5 JSON libraries on 3 datasets, for deserializing (load) and serializing (dump).

### Libraries
* [json](https://docs.python.org/3/library/json.html)
* [orjson](https://github.com/ijl/orjson)
* [ujson](https://github.com/ultrajson/ultrajson)
* [rapidjson](https://github.com/python-rapidjson/python-rapidjson)
* [simplejson](https://github.com/simplejson/simplejson)

### Datasets
Each of the 3 datasets has 1000 records, selected from the top results of following searches.
* [most-cited](https://inspirehep.net/api/literature?sort=mostcited): most cited records in INSPIRE.
* [random](https://inspirehep.net/api/literature?earliest_date=2015--2020): records with earliest date >= 2015.
* [many-authors](https://inspirehep.net/api/literature?q=ac%20200+&earliest_date=2015--2020): records with more than 200 authors and earliest date >= 2015.

Note that the two latter datasets are effectively random, as no sort order has been specified.

The datasets are too large to be included in this repo, but the `fetch_data.py` script to generate them is present.

### Benchmark

We (de)serialized all records in each of those datasets 5 times, with each library and aggregated the results (`tests.py` script). In order to run it on realistic hardware, we built docker images (see `Dockerfile`) and created jobs to run it on our kubernetes cluster (see `kubernetes.yml`). The results are then processed with `analyze_results.py` to generate the table and plot in the next subsection.

## Results

Dataset|Library|Operation|Average time full dataset
---|---|---|---
random|json|load|2.5716108437627554
random|orjson|load|**1.6769399158656597**
random|ujson|load|2.272227367386222
random|rapidjson|load|2.7491534277796745
random|simplejson|load|2.1333015505224466
many-authors|json|load|76.37307294644415
many-authors|orjson|load|**52.80944381467998**
many-authors|ujson|load|73.78779327683151
many-authors|rapidjson|load|87.51749732345343
many-authors|simplejson|load|63.694295370951295
most-cited|json|load|5.2402846701443195
most-cited|orjson|load|**3.564463946968317**
most-cited|ujson|load|5.013203462585807
most-cited|rapidjson|load|5.926249857991934
most-cited|simplejson|load|4.376293800771236
random|json|dump|3.177771395072341
random|orjson|dump|**0.6636625099927187**
random|ujson|dump|1.833177963271737
random|rapidjson|dump|1.8705584052950144
random|simplejson|dump|4.131725179031491
many-authors|json|dump|90.9779446143657
many-authors|orjson|dump|**18.102600283920765**
many-authors|ujson|dump|52.41105090640485
many-authors|rapidjson|dump|50.736949410289526
many-authors|simplejson|dump|113.3073948584497
most-cited|json|dump|6.394005540758371
most-cited|orjson|dump|**1.2374399024993181**
most-cited|ujson|dump|3.6458546351641417
most-cited|rapidjson|dump|3.466435482725501
most-cited|simplejson|dump|8.050390353426337

![Plot of results](https://github.com/inspirehep/json-benchmark/blob/main/results.png)

The green bar is the average, the orange bar is the median. The boxes go from first to third quartile, and the whiskers from minimum to maximum.

`orjson` is the clear winner. Serializing large records is particularly impressive.

## JSON schema validation

We're currently using [jsonschema](https://github.com/Julian/jsonschema) for validation. We looked at two other libraries:
* [fastjsonschema](https://github.com/horejsek/python-fastjsonschema/)
* [jsonschema-rs](https://github.com/Stranger6667/jsonschema-rs/tree/master/python)

## fastjsonschema

This is a pure-python implementation, which precompiles the schema into a validator so is in principle much faster than the library we're currently using. While this is true for a small record where we found a 10x performance increase, a very large record resulted in very similar running times. Investigating further, we found [a critical bug](https://github.com/horejsek/python-fastjsonschema/issues/107) preventing us from using it right now.

## jsonschema-rs

This is a rust implementation, which posts very impressive benchmarks. However, it doesn't work for us currently as it doesn't allow custom `format` validators. We should look at it again when it's more mature.
