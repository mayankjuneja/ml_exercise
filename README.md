{
	// Input source has config options like
	//		type:  could be one of file, database, hive, s3 file etc
	// 		Based on the input type, we can have more config options, e.g.
	//			for type="file":
	//				"location": location of the file
	//			for type="database":
	//				"credentials": db credentials
	//				"database": database name
	//				"table": table name
	"input_source": {
		"type": "file",
		"location": "data/input.csv"
	},

	// Output sink has config options like
	//		type:  could be one of file, database, hive, s3 file etc
	// 		Based on the output type, we can have more config options, e.g.
	//			for type="file":
	//				"location": location of the file
	//			for type="database":
	//				"credentials": db credentials
	//				"database": database name
	//				"table": table name
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
