
# Computation Graph

The computation graph is implemented by a set of python objects that derive from a common base class.
Data are represented as numpy arrays and arithmetic is performed by numpy.
This base class supports a set of built-in commutative operations, typically within a Region-of-Interest (ROI).
All relevant data (e.g. accumulators) is stored within the object.

## Built-in primitive operations

These apply to any data object.

ROI specification,
sum, (mean), standard deviation

## Built-in complex operations

(1-dimensional data support?)

Contour projection,
Peak Finder,
Blob Finder,
Droplet Finder

## User-supplied code

The user can install packages using Conda.
The user can provide Python source code to be imported into the computation graph and executed by objects.

When the user starts a session they go through steps to define the new packages or code.
The Python Conda environment is located on an NFS mount point that accessible to all cluster nodes.
Use supplied code is copied with directory structure intact to a well-known place.


User-supplied code can cause runtime failures.
Some of these failures cannot be detected by the Graph Manager.
Such errors can only be detected by a Worker or Reducer.
These components can invalidate a graph when it is discovered to be bad,
and return to using the previously known good graph.


## Server psueodcode

This is a simple server.
It accepts a computation graph once and edecutes it repeatedly.


```
import AMI_server as AMI

graph = AMI.workerGraph()
for element in graph.elements:
  element.initializeComputation()


nextSampleTime = 0
samplingInterval = 100

if True:
  eventData = AMI.ingestEvent()
  result = {}
  for element in graph.elements:
    result.update(element.executeComputation(eventData))
  timestamp = eventData['timestamp']
  if timestamp >= nextSampleTime:
    AMI.submitResultToCollector(result)
    nextSampleTime = timestamp + samplingInterval

```

## Client pseudocode

This pseudocode includes graph creation which would normally be done by the graph manager.
This client corresponds to an Env display from AMI-1 with a single data field.

```
import AMI_client as AMI

def workerGraph():
  graph = AMI.Graph('workerGraph_Env_one_scalar')
  dataPoint = AMI.Point('field0')
  dataPoint.setMean()
  graph.add(dataPoint)
  graph.add(AMI.Point('normalizeField'))
  graph.add(AMI.Point('weightField'))
  graph.add(AMI.Point('timestamp'))
  return graph

def normalizedWeighted(x, normalize, weight):
  return x / normalize * weight


graph = workerGraph()
AMI.submitGraphToManager(graph)

while(True):
  data = AMI.displayResult() # returns data from pub/sub results
  x = data['timestamp']
  y = normalizedWeighted(data['field0.mean.0'], data['normalizeField'], data['weightField'])
  print x, y

```
