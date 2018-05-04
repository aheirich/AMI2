# Overview

AMI2 is a distributed visualization system for use with LCLS-II Free Electron Laser.
It is a rewrite of the previous AMI package.

There are two implementations:
a [Legion based implementation](legion_design.md)
and a [generic implementation](generic_design.md).

## Data flow
Please see Figure 1: system data flow.

Frames of instrument telemetry enter the system through a Data Source.
At SLAC the SharedMemoryDataSource receives XTC telemetry from the Data Acquisition system delivered by RDMA.
A FileDataSource drives the system in offline mode.
The system can be extended with new data sources (e.g. xyzDataSource).

A resilient distributed in-memory storage system (E.g. Redis, Legion) is used for the control and data planes.
Telemetry data resides in a local store within a node.
Computational results and control signals reside in a global store.

Each telemetry frame is processed by a different worker.
Each cluster node supports multiple workers, typically one per core.
The cluster can be scaled to support arbitrarily high data rates.

A worker processes a telemetry frame by feeding the data to a Computation Graph which is a series of transformations.
The computation graph is defined by the Graph Manager according to requests from clients.
It is implemented as a python program that is assembled and optimized by the Graph Manager.
Computational results are written by the worker to the global store.

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
[Workers](worker.md) execute the computation graph on the input data and write the results to the global store.


### Graph Manager
[Graph manager](graph_manager.md) manipulates and optimizes the computation graph.
May be replicated (not distributed) in a large scale system.
The graph definition is stored in the global store.

### Client
[Client processes](client.md) acquire data for visualization or control.
#### GUI Client
Python/Qt client process that sends requests to the Graph Manager and receives data from Feature store.
#### Web Browser Client
Javascript client ([Lexicon](lexicon.md), D3.js)
#### Device Client
Clients may play other roles such as device controllers.

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

[Robust to node or process failure, recover from crash](fault_tolerance.md)

Scriptable, can log/control from logs/scripts

Multiple users can simultaneously edit the computation graph (at low rates)

Scalable to clusters of any size including supercomputers

Drive it online from shared memory event mechanism, or offline from a file

Portable, no Psana dependencies (or isolate them), hardware agnostic Linux/IA, any network

Follow well defined coding conventions, good project hygiene and testing

Extensible - new clients, new GUI elements, new Computation Graph operations, new data sources

Two versions, [one with Legion](legion_design.md) and [one without](generic_design.md)

Support Epics protocol to send data to clients, also for clients to make requests

"sum all", "pick 1", "sum 1" style calculations

## First test

The first test is a generic use case of the most common features, driven from
a canned example.
This should run on a cluster or on a single machine.

Starting from scratch, install the software and start it running.
Use an offline data source to drive a standard interaction.
Open a GUI client that acquires 2D sensor image data.
Select a region from the sensor image.
Plot the mean pixel value of this region across time in a strip chart recorder.
Verify the data visualization is corrent.
Shut the system down cleanly.


