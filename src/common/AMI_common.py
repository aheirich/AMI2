#
# AMI_common.py
#

import numpy
import pickle
import math


###
### graphs
###


class Graph(object):
  
  def __init__(self, name):
    self.name = name
    self.elements = []
  
  def serialize(self):
    filename = "controlStore_" + self.__class__.__name__ + ".dat"
    print(filename)
    pickle.dump(self, open(filename, "wb"))
  
  def deserialize(self):
    filename = "controlStore_" + self.__class__.__name__ + ".dat"
    print(filename)
    return pickle.load(open(filename, "rb"))
  
  def add(self, element):
    self.elements.append(element)
  
  def broadcast(self):
    self.serialize()






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

  def length(self):
    return 1

  def allocateData(self):
    return numpy.zeros((1))

class VectorDataPoint(DataPoint):
  
  def __init__(self, *args):
    super(ScalarDataPoint, self).__init__(1)
    self.dimensions = [ args[0] ]

  def length(self):
    return self.dimensions[0]

  def allocateData(self):
    return numpy.zeros(self.length())


###
### graph elements
###

class GraphElement(object):
  
  def __init__(self, *args, **kwargs):
    self.name = args[0]
    self.dimensions = []
    self.dataType = ScalarDataPoint()
    #
    self.ROI = []
    self.filter = None
    self.mean = False
    self.sum = False
    self.standardDeviation = False
    self.channel = None
    #
    if kwargs is not None:
      for key, value in kwargs.iteritems():
        eval('self.' + key + ' = ' + value)
    self.data = self.allocateData()

  def dataTypeIs(self, dataType):
    self.dataType = dataType

  def allocateData(self):
    return numpy.zeros(self.shape())
  
  def getData(self):
    pass#TODO
  
  def defaultROI(self):
    return [0]
  
  def shape(self):
    return (1)

  def setROI(self, roi):
    self.ROI.append(roi)

  def setFilter(self, filter):
    self.filter = filter

  def setMean(self):
    self.mean = True

  def setSum(self):
    self.sum = True

  def setStandardDeviation(self):
    self.standardDeviation = True
    self.sumSquaredDifferences = self.allocateData()
# standard deviation is sqrt( sumSquaredDifferences / (count-1) )

  def setChannel(self, channel):
    self.channel = channel

  def initializeComputation(self):
    self.allocateData()
  
  def resultName(self, prefix, roiIndex):
    return self.name + '.' + prefix + '.' + str(roiIndex)
  
  # TODO this method is too long
  def computation(self, data, roi, roiIndex):
    result = {}
    if self.sum or self.mean or self.standardDeviation:
      sum = self.dataType.allocateData()
      if len(roi) > 1:
        for i in range(roi[0], roi[2] + 1):
          for j in range(roi[1], roi[3] + 1):
            sum = sum + data[i][j]
      else:
        sum = sum + data
      if self.sum: result[self.resultName('sum', roiIndex)] = sum
      if len(roi) > 1:
        mean = sum / ((roi[2] - roi[0] + 1) * (roi[3] - roi[1] + 1))
      else:
        mean = sum
      if self.mean: result[self.resultName('mean', roiIndex)] = mean
      if self.standardDeviation:
        sumSquaredDifferences = self.dataType.allocateData()
        for i in range(roi[0], roi[2]):
          for j in range(roi[1], roi[3]):
            difference = data[i][j] - mean
            sumSquaredDifferences = sumSquaredDifferences + difference * difference
        result[self.resultName('standardDeviation', roiIndex)] = math.sqrt(sumSquaredDifferences / (numPoints - 1))
    else:
      result = { self.name : data }
    return result

  def executeComputation(self, telemetryFrame):
    data = telemetryFrame[self.name]
    if self.filter is not None:
      if self.filter(data) is False:
        return {}
    result = {}
    index = 0
    for roi in self.ROI:
      result.update(self.computation(data, roi, index))
      index = index + 1
    if len(self.ROI) > 0:
      return result
    return self.computation(data, self.defaultROI(), 0)

    

  def finalizeComputation(self):
    pass




class Tensor(GraphElement):
  
  def __init__(self, *args, **kwargs):
    super(Tensor, self).__init__(args[0], kwargs)

class Tensor0D(Tensor):
  
  def __init__(self, *args, **kwargs):
    super(Tensor0D, self).__init__(args[0], kwargs)

class Point(Tensor0D):
  
  def __init__(self, *args, **kwargs):
    super(Point, self).__init__(args[0], kwargs)

class Tensor1D(Tensor):
  
  def __init__(self, *args, **kwargs):
    super(Tensor1D, self).__init__(args[0], kwargs)

  def shape(self):
    return (self.dimensions[0], self.dataType.length())

class Vector(Tensor1D):
  
  def __init__(self, *args, **kwargs):
    super(Vector, self).__init__(args[0], kwargs)

class Tensor2D(Tensor):
  
  def __init__(self, *args, **kwargs):
    super(Tensor2D, self).__init__(args[0], kwargs)
  
  def shape(self):
    return (self.dimensions[0], self.dimensions[1], self.dataType.length())

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


class Image(Tensor2D):
  
  def __init__(self, *args, **kwargs):
    super(Image, self).__init__(args[0], kwargs)

class CSPAD(Image, Sensor):
  
  def __init__(self, *args, **kwargs):
    Image.__init__(self, args[0], kwargs)
    Sensor.__init__(self, args[0], kwargs)




