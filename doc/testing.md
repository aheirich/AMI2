# Testing

Test suites will pass whether they are run on a single computer or on a cluster.

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

## More tests

concurrent graph modification

scaling and throughput

scripted tests using FileClients

scripted/manual tests using non-FileClients

