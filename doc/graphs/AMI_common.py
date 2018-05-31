#
# AMI_common.py
#

import numpy
import pickle


###
### graphs
###

def receiveGraphByClass(className):
  graph = eval(className + '("' + className +  '")')
  return graph.deserialize()


class Graph(object):
  
  def __init__(self, name):
    self.name = name
  
  def serialize(self):
    filename = "controlStore_" + self.__class__.__name__ + ".dat"
    print(filename)
    pickle.dump(self, open(filename, "wb"))
  
  def deserialize(self):
    filename = "controlStore_" + self.__class__.__name__ + ".dat"
    print(filename)
    return pickle.load(open(filename, "rb"))
  
  elements = []
  def add(self, element):
    self.elements.append(element)
  
  def broadcast(self):
    self.serialize()




class ComputationGraph(Graph):
  
  def __init__(self, name):
    super(ComputationGraph, self).__init__(name)

  def initialize(self):
    for element in self.elements:
      element.initializeComputation()

  def execute(self, telemetryFrame):
    for element in self.elements:
      element.executeComputation(telemetryFrame)

  def finalize(self):
    for element in self.elements:
      element.finalizeComputation()


class CollectorGraph(Graph):
  
  def __init__(self, name):
    super(CollectorGraph, self).__init__(name)

  def initialize(self):
    for element in self.elements:
      element.initializeCollector()

  def execute(self, computationResult):
    for element in self.elements:
      element.executeCollector(computationResult)

  def finalize(self):
    for element in self.elements:
      element.finalizeCollector()


class DisplayGraph(Graph):
  
  def __init__(self, name):
    super(DisplayGraph, self).__init__(name)


###
### data point
###

class DataPoint(object):

  def __init__(self, numDimensions=0):
    self.numDimensions = numDimensions

class ScalarDataPoint(DataPoint):
  
  def __init__(self):
    super(ScalarDataPoint, self).__init__(0)
    self.dimensions = []

class VectorDataPoint(DataPoint):
  
  def __init__(self, *args):
    super(ScalarDataPoint, self).__init__(1)
    self.dimensions = [ args[0] ]



###
### graph elements
###

class GraphElement(object):
  
  def __init__(self, *args, **kwargs):
    self.name = args[0]
    self.dimensions = []
    self.ROI = None
    self.exponentialDecay = None
    self.timeAverage = None
    self.dataType = ScalarDataPoint()
    if kwargs is not None:
      for key, value in kwargs.iteritems():
        eval('self.' + key + ' = ' + value)
  
#  def constructorArguments(self):
#    result = "'" + self.name + "'" + ', { '
#    result = result + "'dimensions' : " + str(self.dimensions)
#    if self.ROI is not None:
#      result = result + ", 'ROI' : " + str(self.ROI)
#    if self.exponentialDecay is not None:
#      result = result + ", 'exponentialDecay' : " + str(self.exponentialDecay)
#    if self.timeAverage is not None:
#      result = result + ", 'timeAverage' : " + str(self.timeAverage)
#    result = result + ' }'
#    return result
#
#  def selfDeclaration(self):
#    declaration = self.name + ' = AMI.' + self.__class__.__name__ + '(' + self.constructorArguments() + ')'
#    return declaration

  def maxROI(self):
    result = [0] * len(self.dimensions)
    for i in self.dimensions:
      result.append(i - 1)
    return result

  def addROI(self, computation, dataType):
    self.ROI = [ computation, dataType, self.maxROI(), None ]

  def mean(self):
    if self.ROI is not None:
      ROI = self.ROI[1]
      return 1#TODO
  
  def addExponentialDecay(self, decay):
    accumulator = self.allocateData()
    self.exponentialDecay = [ decay, accumulator ]

  def addTimeAverage(self):
    accumulator = self.allocateData()
    self.timeAverage = [ 0, accumulator ]

  def dataTypeIs(self, dataType):
    self.dataType = dataType

  def allocateData(self):
    if self.dataType.__class__ == ScalarDataPoint:
      if len(self.dimensions) == 0:
        return numpy.zeros((1))
      elif len(self.dimensions) == 1:
        return numpy.zeros((self.dimensions[0]))
      elif len(self.dimensions) == 2:
        return numpy.zeros((self.dimensions[0], self.dimensions[1]))
    elif self.dataType.__class__ == VectorDataPoint:
      if len(self.dimensions) == 0:
        return numpy.zeros((self.dataType.dimensions[0]))
      elif len(self.dimensions) == 1:
        return numpy.zeros((self.dimensions[0], self.dataType.dimensions[0]))
      elif len(self.dimensions) == 2:
        return numpy.zeros((self.dimensions[0], self.dimensions[1], self.dataType.dimensions[0]))



class Tensor(GraphElement):
  
  def __init__(self, *args, **kwargs):
    super(Tensor, self).__init__(args[0], kwargs)

class Tensor0D(Tensor):
  
  def __init__(self, *args, **kwargs):
    super(Tensor0D, self).__init__(args[0], kwargs)
    self.data = self.allocateData()

class Point(Tensor0D):
  
  def __init__(self, *args, **kwargs):
    super(Point, self).__init__(args[0], kwargs)

class Tensor1D(Tensor):
  
  def __init__(self, *args, **kwargs):
    super(Tensor1D, self).__init__(args[0], kwargs)
    self.data = self.allocateData()

class Vector(Tensor1D):
  
  def __init__(self, *args, **kwargs):
    super(Vector, self).__init__(args[0], kwargs)

class Tensor2D(Tensor):
  
  def __init__(self, *args, **kwargs):
    super(Tensor2D, self).__init__(args[0], kwargs)
    self.data = self.allocateData()

class Image(Tensor2D):
  
  def __init__(self, *args, **kwargs):
    super(Image, self).__init__(args[0], kwargs)

class VectorField1D(Tensor1D):
  
  def __init__(self, *args, **kwargs):
    super(VectorField1D, self).__init__(args[0], kwargs)
    self.dataTypeIs(VectorDataPoint())

class VectorField2D(Tensor2D):
  
  def __init__(self, *args, **kwargs):
    super(VectorField2D, self).__init__(args[0], kwargs)
    self.dataTypeIs(VectorDataPoint())


###
### sensors
###

class Sensor(object):

  def __init__(self, *args, **kwargs):
    pass

  def initializeComputation(self):
    pass

  def executeComputation(self, telemetryFrame):
    self.data = telemetryFrame[self.name]
    if self.ROI is not None:
      computation, dataType, ROI, dummy = self.ROI
      buffer = eval(dataType + '("' + self.name + '")')
      eval('self.' + computation + '(buffer)')
      self.ROI[3] = buffer
    if self.exponentialDecay is not None:
      decay, accumulator = self.exponentialDecay
      accumulator = numpy.add(decay * accumulator, (1.0 - decay) * self.data)
      self.exponentialDecay[1] = accumulator
    if self.timeAverage is not None:
      numPoints, accumulator = self.timeAverage
      accumulator = accumulator + self.data
      self.timeAverage = [ numPoints + 1, accumulator ]

  def finalizeComputation(self):
    pass

class CSPAD(Image, Sensor):
  
  def __init__(self, *args, **kwargs):
    Image.__init__(self, args[0], kwargs)
    Sensor.__init__(self, args[0], kwargs)


###
### collectors
###

class Collector(object):

  def __init__(self, *args, **kwargs):
    pass

  def initializeCollector(self):
    pass

  def executeCollector(self, computationResult):
    pass

  def finalizeCollector(self):
    pass


class StripChart(Vector, Collector):
  
  def __init__(self, *args, **kwargs):
    Vector.__init__(self, args[0], kwargs)
    Collector.__init__(self, args[0], kwargs)


