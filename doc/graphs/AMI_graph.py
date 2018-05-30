#
# AMI_graph.py
#

import numpy

## TODO Seprate these between called from client and called from graph

## Q what about vector data as opposed to scalar data?


class DATATYPE(object):
  
  def __init__(self, name):
    self.name = name
    self.RHS = 0
    self.ROI = None
    self.computeMeanInROI = False
    self.decayExponent = 0
    self.timeAverageNumPoints = 0
    self.sourceDataName = None
    self.dimensions = 0

  ## options set by clients:

  ## computation option
  def decayExponential(self, exponent):
    self.decayExponent = exponent
  
  ## collector option
  def timeAverage(self, numPoints):
    self.timeAverageNumPoints = numPoints
  
  ## computation option
  def meanInROI(self):
    self.computeMeanInROI = True

  #######

  def roiName(self):
    return '_' + self.name + '_ROI'
  
  def accumulatorName(self):
    return '_' + self.name + '_accumulator'
  
  def meanInROIName(self):
    return '_meanIn' + self.roiName()
  
  def computationPreambleDecay(self):
    return self.accumulatorName() + ' = ' + str(self.RHS)

  def computationPreambleROI(self):
    return self.roiName() + ' = ' + str(self.ROI)

  def computationPreamble(self):
    result = []
    if self.decayExponent > 0 and self.decayExponent < 1:
      result.append(self.computationPreambleDecay())
    if self.ROI is not None:
      result.append(self.computationPreambleROI())
    return result

  def stripChartName(self):
    return '_' + self.sourceDataName + '_stripChartBuffer'

  def collectorPreamble(self):
    return ''

  def generateCollector(self):
    return ''

  def generateMergeSeries(self):
    return self.accumulatorName() + ' = AMI.mergeSeries(' + self.name + ', ' + self.accumulatorName() + ', ' + str(self.decayExponent) + ')'
  
  def generateComputeMeanInROI(self):
    return self.meanInROIName() + ' = AMI.meanInROI(' + self.name + ', ' + self.roiName() + ')'

  def computationGraph(self):
    result = [ self.name + ' = telemetryFrame[ "' + self.name + '" ]' ]
    if self.decayExponent > 0 and self.decayExponent < 1:
      result.append(self.generateMergeSeries())
    if self.computeMeanInROI:
      result.append(self.generateComputeMeanInROI())
    return result

  def displayPreamble(self):
    return []

  def displayGraph(self):
    return []


class TENSOR(DATATYPE):
  def __init__(self, name):
    super(TENSOR, self).__init__(name)

class TENSOR0D(TENSOR):
  def __init__(self, name):
    super(TENSOR0D, self).__init__(name)

  def initializeRHS(self):
    return '0'

class POINT(TENSOR0D):

  def __init__(self, name, size=0):
    super(POINT, self).__init__(name)


class TENSOR1D(TENSOR):
  
  def __init__(self, name, size=0):
    super(TENSOR1D, self).__init__(name)
    self.size = size
    self.RHS = 'numpy.array([0] * ' + str(self.size) + ')'
    self.dimensions = 1

  def bounds(self):
    return { 'xMin' : 0, 'xMax' : self.size - 1 }

class VECTOR(TENSOR1D):

  def __init__(self, name, size=0):
    super(VECTOR, self).__init__(name)

class StripChart(VECTOR):

  def __init__(self, scalarDataType, size=0):
    super(StripChart, self).__init__(scalarDataType.name)
    self.size = size
    self.RHS = 'numpy.array([0] * ' + str(self.size) + ')'
    self.sourceDataName = self.scalarDataName(scalarDataType)
    self.sourceData = scalarDataType
  
  def scalarDataName(self, scalarDataType):
    if scalarDataType.dimensions <= 1:
      return scalarDataType.name
    if scalarDataType.dimensions == 2:
      if scalarDataType.computeMeanInROI:
        return scalarDataType.meanInROIName()
      if scalarDataType.timeAverageNumPoints > 0:
        return scalarDataType.timeAveragedName()
    return None
  
  def timeAveragedName(self):
    return '_timeAveraged_' + str(self.sourceDataName) + '_stripChartBuffer'

  def collectorPreamble(self):
    result = []
    result.append(self.stripChartName() + ' = []')
    result.append(self.stripChartName() + 'Width = ' + str(self.size))
    if self.timeAverageNumPoints > 0:
      result.append(self.stripChartName() + 'RollingSum = 0')
      result.append(self.timeAveragedName() + ' = []')
      result.append(self.timeAveragedName() + 'Width = ' + str(self.timeAverageNumPoints))
    return result

  def collectorGraph(self):
    result = ['if len(' + self.stripChartName() + ') >= ' + self.stripChartName() + 'Width:']
    result.append('  ' + self.stripChartName() + 'RollingSum = ' + self.stripChartName() + 'RollingSum - ' + self.stripChartName() + '[0]')
    result.append('  ' + self.stripChartName() + ' = ' + self.stripChartName() + '[1:]')
    result.append('  ' + self.sourceData.meanInROIName() + ' = computationResult[ "' + self.sourceData.meanInROIName() + '" ]')
    result.append('  ' + self.stripChartName() + '.append(' + self.sourceData.meanInROIName() + ')')
    result.append('  ' + self.stripChartName() + 'RollingSum = ' + self.stripChartName() + 'RollingSum + ' + self.sourceData.meanInROIName())

    if self.timeAverageNumPoints > 0:
      result.append('  ' + 'if len(' + self.timeAveragedName() + ') >= ' + self.timeAveragedName() + 'Width:')
      result.append('    ' + self.timeAveragedName() + ' = ' + self.timeAveragedName() + '[1:]')
      result.append('    ' + self.timeAveragedName() + '.append(' + self.stripChartName() + 'RollingSum / len(' + self.stripChartName() + '))')

    return result


class TENSOR2D(TENSOR):
  
  def __init__(self, name, rows=0, columns=0):
    super(TENSOR2D, self).__init__(name)
    self.rows = rows
    self.columns = columns
    self.RHS = 'numpy.array([0] * ' + str(self.rows * self.columns) + ')'
    self.dimensions = 2
  
  def bounds(self):
    return { 'xMin' : 0, 'xMax' : self.columns - 1, 'yMin' : 0, 'yMax' : self.rows - 1 }


class IMAGE(TENSOR2D):

  def __init__(self, name, rows, columns):
    super(IMAGE, self).__init__(name, rows, columns)

class CSPAD(IMAGE):

  def __init__(self, name, rows, columns):
    super(CSPAD, self).__init__(name, rows, columns)
    self.ROI = [ 0, 0, columns - 1, rows - 1 ]






def ingestTelemetryFrame():
  return { 'cspad' : numpy.array([ [0] * 1048576 ]) }

def getComputationResult():
  return {}

def getCollectorResult():
  return {}

def computationResultIs(result):
  # if result is {} do nothing else pass it to a collector
  pass

def collectorResultIs(result):
  pass

gDisplayResult = None
gDisplayResultMutex = None

def displayResultIs(result):
  global gDisplayResult
  global gDisplayResultMutex
  # acquire mutex
  gDisplayResult = result
# release mutex

def displayResult():
  # acquire mutex
  result = gDisplayResult;
  # release mutex
  return result

def mergeSeries(cspad, series, decayExponent):
  return numpy.add(cspad * (1.0 - decayExponent), series * decayExponent)

def scaleCspad(cspad, scale):
  return cspad * scale

def meanInROI(field, roi):
  # call to C++ here?
  return 1

def dataSources():
  # return a list of available data sources with types
  return [ CSPAD( 'cspad0', 0, 0) ]#TODO

##
## predefined operations
##
## meanInROI
## decayExponential
## timeAverage
##


computations = []

def addComputation(computation):
  global computations
  computations.append(computation)

collectors = []

def addCollector(collector):
  global collectors
  collectors.append(collector)

displays = []

def addDisplay(display):
  global displays
  displays.append(display)

##

def computationGraph():
  result = []
  for computation in computations:
    result = result + computation.computationPreamble()
    result = result + computation.computationGraph()
  return result

def collectorGraph():
  result = []
  for collector in collectors:
    result = result + collector.collectorPreamble()
    result = result + collector.collectorGraph()
  return result

def displayGraph():
  result = []
  for display in displays:
    result = result + display.displayPreamble()
    result = result + display.displayGraph()
  return result






