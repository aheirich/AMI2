# Worker process

class Worker:

The purpose of the worker process is to apply the current computation graph to a set of telemetry data newly acquired from the local Redis.
The results are written to the global Redis.

class Worker accesses the graph definition from the global Redis and updates its local copy when the graph changes.
When the data source has new data the worker executes the computation graph using the new data as input with results written to the global Redis.

The scalability of the system is not limited by the latency through the worker.
This is because we can increase the number of workers and cluster nodes arbitrarily to support any input data rate.
Nonetheless the graph execution should be done efficiently.
The Graph Manager will optimize the graph before distributing it to the global Redis.

In AMI version 1 the execution graph is a python program and clients may request any valid Python operation to be added to the graph.
