# ml_exercise

### Steps to run evaluator (Python 3.5+)
- Install requirements (`pip install -r requirements.txt`)
- (Optional) The repo consists of dummy models, but in case you want to generate it again, you can run `python generate_models.py`. This will train dummy models, serialize them and save it to the disk (`data` folder).
- `python evaluator.py --config_file config.json`
- For discussions on the extensions given in the problem statement, check this [page](/discussions.md).

#### Sample output:
```
Fetching inputs from data/input.csv, type=file
Running model Linear Regression
80%
Running model Neural Network Regression
82%
Generating data from Neural Network Regression and storing results into data/best_model.txt.
```

### Code Structure
* `evaluator.py` -- main code that has the evaluator logic. This is responsible for reading the configuration file, reading the data and iterating over all the models, finally writing the best results to output sync.
* `config.json` -- json configuration file (look at this [section](#configuration) for detailed description of the configuration options)
* `model.py` -- Consists `TrainedModel` class which is an abstraction on top of a trained model artifcat. It wraps up different model types and exposes common functions like `load`, `save`, `predict`, `evaluate` so that the we don't need custom code for each type of model.
* `generate_models.py` -- Helper script to generate dummy models, serialize and save to disk
* `exceptions.py` -- custom exceptions
* `data` -- Contains serialized dummy models and sample input files needed for testing the evaluator.

### Configuration
The different parameters can be changed easily by updating the json file (can also be generated as part of some other upstream process). This makes changing parameters like input sources, output sinks, list of models, metric etc customizable without changing the core evaluator.

```
{
        // Input source has config options like
        //              type:  could be one of file, database, hive, s3 file etc
        //              Based on the input type, we can have more config options, e.g.
        //                      for type="file":
        //                              "location": location of the file
        //                      for type="database":
        //                              "credentials": db credentials
        //                              "database": database name
        //                              "table": table name
        "input_source": {
                "type": "file",
                "location": "data/input.csv"
        },

        // Output sink has config options like
        //              type:  could be one of file, database, hive, s3 file etc
        //              Based on the output type, we can have more config options, e.g.
        //                      for type="file":
        //                              "location": location of the file
        //                      for type="database":
        //                              "credentials": db credentials
        //                              "database": database name
        //                              "table": table name
        "output_sink": {
                "type": "file",
                "location": "data/best_model.bin"
        },

        // Input features: List of input features to be used for calling the predict/evaluate function. This will usually map to columns of the input data
        "input_features": ["age", "sex", "bmi", "bp", "s1", "s2", "s3", "s4", "s5", "s6"],

        // Ouptut column name: Column that consists of the target values (y). Assumption here is that the target value is part of the input data provided
        "output_label": "target",

        // models: List of models to be used for evaluation. These are basically paths of the serialized models to be used (each one is of instance type `TrainedModel`))
        "models": ["data/linear_regression.bin", "data/neural_network_regression.bin"],

        // metric: Metric name that should be used from evaluating and picking up the best model
        "metric": "r2"
}
```
