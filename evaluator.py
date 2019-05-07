"""
Assumptions:
Only talking about columnar dataframes, where input
can be represented as a dataframe
Input data has a column which has the target label/value
of the example, which will be used to measure the performance of the model
The platform has a CLI interface which takes in list of models to be evaluated,
input data source, output data sink, input feature names, output label
Assumption is data fits in memory
"""

import json
import click
import pandas as pd
from typing import Dict, Tuple
from model import TrainedModel
from exceptions import ConfigValidationException


class Evaluator(object):

    def __init__(self, config: Dict) -> None:
        self.config = config

    def validate_config(self) -> None:
        """
        Runs common validations on the config file, like
        - all the required keys are present
        - the config values have the right data format
        """
        keys_format = {
            'input_source': dict,
            'output_sink': dict,
            'input_features': list,
            'output_label': str,
            'models': list,
            'metric': str
        }

        for key, data_type in keys_format.items():
            # Check for presence of required keys
            if key not in self.config:
                raise ConfigValidationException(f"{key} not present in config \
                                                    file")
            # Check if the keys have correct data type
            if type(self.config[key]) is not data_type:
                raise ConfigValidationException(f"{key} not in correct format, \
                                                should be of type {data_type}")

    def _load_input_file(self, input_source: Dict) -> pd.DataFrame:
        """
        Loads the input from a file data source and returns as a dataframe
        """
        print(f"Fetching inputs from {input_source['location']}, type=file")
        df = pd.read_csv(input_source['location'])
        return df

    def _load_input_database(self, input_source: Dict) -> pd.DataFrame:
        """
        Loads the input from a database table source and returns as a dataframe
        The input source configuration can have options like database
        credentials, table name etc
        """
        # Not implemented
        pass

    def load_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Loads the input features and the target variable as per the config
        options
        Based on the input source type, calls the relevant helper functions.
        """
        input_source = self.config['input_source']
        input_features = self.config['input_features']
        output_label = self.config['output_label']
        input_type = input_source['type']

        if input_type == "file":
            df = self._load_input_file(input_source)
        elif input_type == "database":
            df = self._load_input_database(input_source)

        # Reorder columns based on input_features
        input_data = df[input_features]

        # Get the target variable
        output = df[[output_label]]
        return input_data, output

    def _write_best_model_file(self, output_sink: Dict, best_model: Dict) -> None:  # noqa
        """
        Writes the best model to a file. Uses the TrainedModel class to dump
        the model to disk (using joblib)
        """
        model = best_model["model"]
        result = best_model["result"]
        location = output_sink["location"]
        print(f"Generating data from {model.metadata['name']} and storing results into {location}.")  # noqa
        with open(location, 'w') as f:
            f.write(f"{result}%")

    def _write_best_model_database(self, output_sink: Dict, best_model: Dict) -> None:  # noqa
        """
        Writes the best model to a database.
        The output sink  configuration can have options like database
        credentials, table name etc
        """
        # Not Implemented
        pass

    def write_best_model(self, best_model: Dict) -> None:
        """
        Takes the best model found and writes it as per the output
        sink configuration.
        Based on the output sink type, calls the relevant helper function
        """
        output_sink = self.config["output_sink"]
        output_type = output_sink["type"]

        if output_type == "file":
            self._write_best_model_file(output_sink, best_model)
        elif output_type == "database":
            self._write_best_model_database(output_sink, best_model)

    def run(self) -> None:
        # We will load the data first and then iteratively run
        # the models and store the predictions
        input_data, actual_output = self.load_data()
        model_paths = self.config["models"]
        metric = self.config["metric"]
        best_model = {
            "model": None,
            "result": -1
        }
        for model_path in model_paths:
            model = TrainedModel.load(model_path)
            name = model.metadata["name"]
            print(f"Running model {name}",)
            result = model.evaluate(input_data, actual_output, metric)
            print(f"{result}%")
            if result > best_model["result"]:
                best_model["model"] = model
                best_model["result"] = result

        self.write_best_model(best_model)


@click.command()
@click.option('--config_file')
def run(config_file):
    with open(config_file) as f:
        config = json.load(f)

    evaluator = Evaluator(config)
    evaluator.validate_config()
    evaluator.run()


if __name__ == "__main__":
    run()
