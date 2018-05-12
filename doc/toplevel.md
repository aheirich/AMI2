# Overview

AMI2 is a distributed visualization system for use with LCLS-II Free Electron Laser.
It is a rewrite of the previous AMI package.

There are two designs:
a [Legion based design](legion_design.md)
and a [Redis based design](redis_design.md).
The reason for two designs is that Legion is currently an experimental open source programming platform without
a guarantee of long term support.
The Redis design will incorporate existing stable open source software packages where appropriate.

[Clients](client.md) interact with the rest of the system through communication protocols and
are oblivious to the difference between the two designs.

[Testing](testing.md) is described here.

## Data flow
Please see Figure 1: system data flow.

Frames of instrument telemetry enter the system through a Data Source.
At SLAC the SharedMemoryDataSource receives XTC telemetry from the Data Acquisition system delivered by RDMA.
A FileDataSource drives the system in offline mode.
The system can be extended with new data sources (e.g. xyzDataSource).

A resilient distributed in-memory storage system (E.g. Redis, Legion) is used for the control and data planes.
Telemetry data resides in a local store within a node.
Computational results and control signals reside in a global store.
Process heartbeats are monitored and failed processes are automatically restarted.
The process stores all volatile state in the resilient stores so it can reload that state when it restarts.

Each telemetry frame is processed by a different worker.
Each cluster node supports multiple workers, typically one per core.
The cluster can be scaled to support arbitrarily high data rates.

A worker processes a telemetry frame by feeding the data to a computatiog graph which is a series of transformations.
The computation graph is defined by the Graph Manager according to requests from clients.
It is implemented as a python program that is assembled and optimized by the Graph Manager.
The program can compute sums of data across frames.
The worker sends outputs of the computation graph to the Collector.

A Collector receives outputs from a set of workers.
It filters and buffers the outputs according to a collector graph that is similar to the computation graph.
The collector graph is implemented as a python program and is maintained by the Graph Manager in response to client requests.

The purpose of the collector graph is to buffer and filter data before passing it to the Result store.
The collector graph reduces the data rate from the workers to the Heartbeat Rate of the system.
The Heartbeat Rate is the perceptual thershold of 20 Hz.
This is the rate at which the Result Store is updated and also the Clients.


Clients may be GUIs, web browsers, devices, or file proxies.
Clients requests computations from the Graph Manager and subscribe to result channels from the global store.





## System Diagram

<img src="images/AMI2_system_diagram/AMI2_system_diagram.001.jpeg" width=800>

### Data Acquisition (DAC)
Data delivery events from sensors, distributed round-robin to nodes via Infiniband RDMA.

### DataSource
[DataSources](data_source.md) provide telemetry data to the system.
#### SharedMemoryDataSource
Transfers incoming sensor data to the local store.
#### FileDataSource
Replays sensor data stored in a file.
#### xyzDataSource
User extended data source

### Worker
[Workers](worker.md) execute the computation graph on the telemetry data and send the results to a collector.


### Collector
[Collectors](collector.md) execute the collector graph on worker outputs and writes the results to the global store.
Collectors filter and buffer worker outputs and reduce the data rate to the Heartbeat Rate.

### Graph Manager
[Graph manager](graph_manager.md) manipulates and optimizes the computation graph.
May be replicated (not distributed) in a large scale system.
The graph definition is stored in the global store.

### Client
[Client processes](client.md) acquire data for visualization or control.
Clients may be based on Python/Qt, Web Browsers or Devices.
A FileClient is mainly useful for testing.


### Protocol handlers
Communication between the clients and GraphManager occurs over a [modular protocol](protocol.md).
#### Epics protocol
The Experimental Physics and Industrial Control System (EPICS) is a DOE labs protocol.
#### TCP/IP

### Robustness Monitor
The [Robustness Monitor](robustness.md) monitors the state of the system and restarts failed processes.
It is in turn monitored by another component.
This guarantees that the system will stay up unless both components fail simultaneously.


## Project Goals

Open Source package for Linux with an installer

[Robust to node or process failure, recover from crash](robust.md)

Scriptable, can log/control from logs/scripts

Multiple users can simultaneously edit the computation graph (at low rates)

Scalable to clusters of any size including supercomputers

Drive it online from shared memory event mechanism, or offline from a file

Portable, no Psana dependencies (or isolate them), hardware agnostic Linux/IA, any network

Follow well defined coding conventions, good project hygiene and testing

Extensible - new clients, new GUI elements, new Computation Graph operations, new data sources

Two versions, [one with Legion](legion_design.md) and [one with Redis](redis_design.md)

Support Epics protocol to send data to clients, also for clients to make requests

Support operations across time:
"sum all", "pick 1", "sum 1" style calculations




