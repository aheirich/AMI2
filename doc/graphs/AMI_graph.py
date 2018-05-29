#
# AMI_graph.py
#

import numpy

def ingestTelemetryFrame():
  return { 'cspad' : numpy.array([ 0 ]) }

def getComputationResult():
  return {}

def getCollectorResult():
  return {}

def computationResultIs(result):
  # if result is {} do nothing else pass it to a collector
  pass

def collectorResultIs(result):
  pass

def displayResultIs(result):
  # hold result data in a buffer for access by the display widgets
  # display widgets ryun in a separate thread/loop, consult the buffer
  # this should work for both pyQt client and browser client (confirm??)
  pass

def mergeCspad(cspad, sum):
  return = sum + cspad

def scaleCspad(cspad, scale):
  return cspad * scale

def meanPixelIntensity(field, roi):
  return 1

