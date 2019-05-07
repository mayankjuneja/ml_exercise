## Discussions

> 1.	How does your design handle the case when source and sink datastores are replaced by Disk storage or MongoDB or Cassandra(NoSQL) ?

The current evaluator can be extended to handle new source and sink datastores by just writing plugins for a new datastore. e.g. if we need to support MongoDB, we will just need to write a plugin in the evaluator which can read the database config and read/write data from the database. On top of plugin, the config file needs to have the right datastore type (`input_source->type` and `input_source->{credentials, table_name, etc}`

> 2.	The logic of prioritizing a particular model might change over the period of time(Say. now the the model with highest precision is selected instead of highest accuracy), What changes are required to achieve the same?

The evaluator supports multiple metrics and configured easily by updating the `metric` key in the config file. Again no change in the code required, only change required is in the config file.

> 3.	What do you do, if the static data stores are replaced by unbounded data streams ? A sample case for a stream dataset would be:
> 
> Inputs:
> 
> { 03:00 PM  Regression: 45%, SVM:60%,ARIMA:71%}
> { 03:05 PM  Regression: 51%, SVM:81%,ARIMA:69%}
> { 03:10 PM  Regression: 84%, SVM:46%,ARIMA:73%}
> …
> 
> Outputs: 
> 
> { 03:05 PM storing output from ARIMA }
> { 03:10 PM storing output from SVM }
> { 03:15 PM storing output from Regression }
> ...

The complete solution will depend on the actual streaming solution. But one option could be to move the evaluator inside the workers who are listening to this stream of data or some async workers that have access to this stream. On receiving a new stream of data, the workers will call the `run` method from the Evaluator class.

> 4.	What if you want to restrict few models to run over datasets ?

The list of models can be controlled by the `models` key in the config file. The evaluator code does not need to be changed if we need to restrict the models to be used.

> 5.	There should be a provision of adding new models to the system over the period of time.?

New models can be easily added to the system. Primary requirement is to serialize the model using the `TrainedModel` class (from `model.py`). As long as that requirement is satisified, adding a new model is as easy as updating the list of models in the config file.
