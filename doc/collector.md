# Collector 

class Collector:

The purpose of the collector is to apply the current collector graph to outputs from multiple Workers.
The collector graph filters and buffers the data to reduce the data rate.
The results are written to the Result store.

The collector graph is a python program.
Clients add operations to the graph by submitting requests to the GraphManager.
This can include arbitrary python code.

class Collector accesses the graph definition from the Control store and updates its local copy when the graph changes.
When the worker has new outputs the collector executes the collector graph with results written to the Result store.



