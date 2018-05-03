# Worker process

class Worker:

The purpose of the worker is to apply the current computation graph to a set of telemetry data newly acquired from the local store.
The results are written to the global store.

The computation graph is a python program.  Clients add operations to the graph by submitting python operations.
This can include arbitrary python code.

class Worker accesses the graph definition from the global store and updates its local copy when the graph changes.
When the data source has new data the worker executes the computation graph using the new data as input with results written to the global store.

The scalability of the system is not limited by the latency through the worker.
This is because we can increase the number of workers and cluster nodes arbitrarily to support any input data rate.
Nonetheless the graph execution should be done efficiently.
The Graph Manager will optimize the graph before distributing it to the global store.


