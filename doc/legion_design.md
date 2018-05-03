# Legion design

<img src="images/AMI2_system_diagram/AMI2_system_diagram.002.jpeg" width=800>
 
In the Legion design all of the components are Legion tasks except for the clients.
The stores are Legion logical regions.

A custom mapper ensures that data sources and workers are mapped together on cluster nodes.
The telemetry local region is partitioned across the cluster nodes.
The Graph Manager and Robustness Monitors are mapped onto one or more additional cluster nodes.

Legion resilience mechanisms ensure that tasks always complete.
A system cron job ensures that Legion is always running.

The control logical regions implements a [key-value store for JSON data](key_value_lr.md).
